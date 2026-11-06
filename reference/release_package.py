"""Actual archive checks. No Azure client, deployment CLI or publisher included."""
import hashlib,json,re,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNNING_PORTAL_HTTP_ADDITIONS=frozenset()
def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(value):
    require(re.fullmatch(r"[0-9a-f]{40}", value), "A full lowercase commit SHA is required")
    return value

def package(app, source, destination, commit):
    sha(commit)
    source, destination = Path(source).resolve(), Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    roots = [source / "dist"] if app == "web" else [source / n for n in (
        "host.json", "package.json", "package-lock.json", "dist", "node_modules")]
    if app == "api":
        roots.append(source / "migrations")
        roots.append(source / "form-templates")
    require(all(p.exists() for p in roots), "Release inputs are missing")
    if app == "web":
        require((source / "dist/index.html").is_file(), "Web index is missing")
    else:
        require(list((source / "dist/src/functions").glob("*.js")), "Function entrypoints are missing")
    archive = destination / "release.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
        for root in roots:
            files = sorted(root.rglob("*")) if root.is_dir() else [root]
            for file in files:
                if ".bin" in file.relative_to(source).parts:
                    continue
                require(not file.is_symlink(), "Symlinks are not allowed in release inputs")
                if not file.is_file():
                    continue
                relative = file.relative_to(source / "dist" if app == "web" else source)
                # Do not ship application tests, source maps or npm executable shims.
                if ".bin" in relative.parts or (relative.parts[0] == "dist" and (
                    ".test." in file.name or file.suffix == ".map")):
                    continue
                entry = zipfile.ZipInfo(relative.as_posix(), (2026, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                output.writestr(entry, file.read_bytes())
    receipt = {"app": app, "sourceSha": commit,
               "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
    (destination / "release.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt

def verify(app, directory, commit, running_portal=False):
    sha(commit)
    directory = Path(directory)
    receipt = json.loads((directory / "release.json").read_text())
    require(receipt == {"app": app, "sourceSha": commit,
                       "sha256": hashlib.sha256((directory / "release.zip").read_bytes()).hexdigest()},
            "Release identity or digest mismatch")
    with zipfile.ZipFile(directory / "release.zip") as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate archive paths")
        for item in archive.infolist():
            require(not item.filename.startswith("/") and ".." not in item.filename.split("/")
                    and "\\" not in item.filename and ":" not in item.filename,
                    "Unsafe archive path")
            require((item.external_attr >> 16) == 0o100644, "Unsafe archive mode")
        require("index.html" in names if app == "web" else
                all(n in names for n in ("host.json", "package.json", "package-lock.json")),
                "Release root is invalid")
        if app != "web":
            shields = ({"AzureWebJobs.portalAccessProvisioningWorker.Disabled": "true",
                        "AzureWebJobs.portalAccessRevocationWorker.Disabled": "true",
                        "AzureWebJobs.employeeMoverRoleWorker.Disabled": "true",
                        "AzureWebJobs.employeeAccountWorker.Disabled": "true",
                        "AzureWebJobs.staffPasswordResetWorker.Disabled": "true"}
                       if app == "directory-worker" else
                       json.loads((ROOT / "config/function-shields.json").read_text())[app])
            registrations = []
            http_registrations = []
            for name in names:
                if name.startswith("dist/") and name.endswith(".js"):
                    code = archive.read(name).decode("utf-8")
                    calls = re.findall(r"\bapp\.(?:http|timer|storageQueue|storageBlob|serviceBusQueue|serviceBusTopic|eventHub|eventGrid|cosmosDB|generic)\s*\(", code)
                    literals = re.findall(r"\bapp\.(?:http|timer|storageQueue|storageBlob|serviceBusQueue|serviceBusTopic|eventHub|eventGrid|cosmosDB|generic)\s*\(\s*['\"]([^'\"]+)['\"]", code)
                    require(len(calls) == len(literals), "Dynamic Function names need explicit commissioning review")
                    registrations.extend(literals)
                    http_registrations.extend(re.findall(r"\bapp\.http\s*\(\s*['\"]([^'\"]+)['\"]", code))
            require(registrations, "No Function registrations found")
            if app == "directory-worker":
                require(sorted(registrations) == ["employeeAccountWorker", "employeeMoverRoleWorker", "portalAccessProvisioningWorker", "portalAccessRevocationWorker", "staffPasswordResetWorker"],
                        "Directory package must contain exactly its five reviewed workers")
                require(not any(re.search(r"\bapp\.http\s*\(", archive.read(n).decode("utf-8"))
                                for n in names if n.startswith("dist/") and n.endswith(".js")),
                        "Directory package cannot contain HTTP handlers")
            # These reviewed handlers belong only to the running-portal publisher,
            # even now that default isolation explicitly shields them.
            require(all(name not in RUNNING_PORTAL_HTTP_ADDITIONS or
                        (running_portal and app == "api" and name in http_registrations)
                        for name in registrations), "Use the running-portal publisher for these HTTP additions")
            additions = RUNNING_PORTAL_HTTP_ADDITIONS if running_portal and app == "api" else frozenset()
            require(len(registrations) == len(set(registrations)), "Duplicate Function registration")
            require(all(shields.get(f"AzureWebJobs.{name}.Disabled") == "true" or
                        (name in additions and name in http_registrations) for name in registrations),
                    "Package contains a Function without a commissioning shield")
    return receipt
