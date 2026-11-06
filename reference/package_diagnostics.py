"""Exact ZIP filesystem comparison evidence. This never authorizes a release."""
import hashlib
import json
from pathlib import PurePosixPath
import re
import stat
import zipfile


def inventory(path):
    files = {}
    directories = set()
    seen = set()
    total = 0
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if len(entries) > 100000:
            raise ValueError("package_diagnostic_entry_limit")
        for entry in entries:
            name = entry.orig_filename
            parts = name.rstrip("/").split("/")
            mode = entry.external_attr >> 16
            if (not name or name != entry.filename or name.startswith("/") or "\\" in name
                    or any(p in ("", ".", "..") for p in parts)
                    or any(ord(c) < 32 for c in name) or ":" in name
                    or str(PurePosixPath(name)) != name.rstrip("/")
                    or name.rstrip("/") in seen or entry.flag_bits & 1
                    or stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)
                    or (entry.is_dir() and entry.file_size != 0)):
                raise ValueError("package_diagnostic_unsafe_entry")
            seen.add(name.rstrip("/"))
            directories.update("/".join(parts[:i]) for i in range(1, len(parts)))
            if entry.is_dir():
                directories.add(name.rstrip("/"))
            total += entry.file_size
            if total > 1024**3:
                raise ValueError("package_diagnostic_expansion_limit")
            if not entry.is_dir():
                hasher = hashlib.sha256()
                with archive.open(entry) as stream:
                    while chunk := stream.read(1024**2):
                        hasher.update(chunk)
                files[name] = hasher.hexdigest()
    if directories & files.keys():
        raise ValueError("package_diagnostic_conflicting_paths")
    return files, directories


def manifest_digest(value):
    # Names are hashed into a deterministic manifest, never printed or uploaded.
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def compare_packages(expected, active, expected_sha256, output):
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("package_diagnostic_invalid_digest")
    expected_raw = hashlib.sha256(expected.read_bytes()).hexdigest()
    if expected_raw != expected_sha256:
        raise ValueError("package_diagnostic_archive_changed")
    active_raw = hashlib.sha256(active.read_bytes()).hexdigest()
    wanted, wanted_dirs = inventory(expected)
    actual, actual_dirs = inventory(active)
    result = {
        "schemaVersion": 1, "diagnosticOnly": True,
        "expectedZipSha256": expected_raw, "activeZipSha256": active_raw,
        "zipBytesMatch": expected_raw == active_raw,
        "expectedFiles": len(wanted), "activeFiles": len(actual),
        "expectedManifestSha256": manifest_digest(wanted), "activeManifestSha256": manifest_digest(actual),
        "expectedTreeSha256": manifest_digest({"files": wanted, "directories": sorted(wanted_dirs)}),
        "activeTreeSha256": manifest_digest({"files": actual, "directories": sorted(actual_dirs)}),
        "directoryTreeMatch": wanted_dirs == actual_dirs,
        "expectedDirectories": len(wanted_dirs), "activeDirectories": len(actual_dirs),
        "fileContentsMatch": wanted == actual,
        "missingFiles": len(wanted.keys() - actual.keys()),
        "extraFiles": len(actual.keys() - wanted.keys()),
        "changedFiles": sum(wanted[n] != actual[n] for n in wanted.keys() & actual.keys()),
    }
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result
