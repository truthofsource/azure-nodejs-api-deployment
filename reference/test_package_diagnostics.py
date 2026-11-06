import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import stat
import warnings
import zipfile

from package_diagnostics import compare_packages, inventory
from content_guard import validate_api_content

POLICY = {"activeApiIdentity": "verified-archive-filesystem-tree-v1"}


class PackageDiagnostics(unittest.TestCase):
    def test_repacked_bytes_are_distinguished_from_content_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected, active, output = (root / n for n in ("expected.zip", "active.zip", "report.json"))
            with zipfile.ZipFile(expected, "w", compression=zipfile.ZIP_STORED) as z:
                z.writestr("dist/private-name.js", "same content")
            with zipfile.ZipFile(active, "w", compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr("dist/private-name.js", "same content")
            digest = hashlib.sha256(expected.read_bytes()).hexdigest()
            result = compare_packages(expected, active, digest, output)
            self.assertFalse(result["zipBytesMatch"])
            self.assertTrue(result["fileContentsMatch"])
            self.assertTrue(result["directoryTreeMatch"])
            validate_api_content(result, POLICY)
            self.assertNotIn("private-name", output.read_text())
            with zipfile.ZipFile(active, "w") as z:
                z.writestr("dist/private-name.js", "modified")
                z.writestr("unexpected", "extra")
            result = compare_packages(expected, active, digest, output)
            self.assertEqual((result["changedFiles"], result["extraFiles"]), (1, 1))
            self.assertFalse(result["fileContentsMatch"])
            with self.assertRaisesRegex(ValueError, "filesystem_mismatch"):
                validate_api_content(result, POLICY)

    def test_explicit_parent_directory_is_equivalent_but_empty_directory_is_not(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected, active, output = (root / n for n in ("expected.zip", "active.zip", "report.json"))
            with zipfile.ZipFile(expected, "w") as z:
                z.writestr("dir/file", "data")
            digest = hashlib.sha256(expected.read_bytes()).hexdigest()
            with zipfile.ZipFile(active, "w") as z:
                z.writestr("dir/", "")
                z.writestr("dir/file", "data")
            validate_api_content(compare_packages(expected, active, digest, output), POLICY)
            with zipfile.ZipFile(active, "a") as z:
                z.writestr("unexpected-empty/", "")
            result = compare_packages(expected, active, digest, output)
            self.assertTrue(result["fileContentsMatch"])
            self.assertFalse(result["directoryTreeMatch"])
            with self.assertRaisesRegex(ValueError, "filesystem_mismatch"):
                validate_api_content(result, POLICY)

    def test_tree_equivalence_needs_the_explicit_reviewed_policy(self):
        comparison = {"fileContentsMatch": True, "directoryTreeMatch": True}
        for policy in ({}, {"activeApiIdentity": "unreviewed"}):
            with self.assertRaisesRegex(ValueError, "not_reviewed"):
                validate_api_content(comparison, policy)
        for key in comparison:
            with self.assertRaisesRegex(ValueError, "filesystem_mismatch"):
                validate_api_content({**comparison, key: "true"}, POLICY)

    def test_special_duplicate_and_conflicting_entries_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "unsafe.zip"
            info = zipfile.ZipInfo("link")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(path, "w") as z:
                z.writestr(info, "target")
            with self.assertRaisesRegex(ValueError, "unsafe_entry"):
                inventory(path)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(path, "w") as z:
                    z.writestr("duplicate", "one")
                    z.writestr("duplicate", "two")
            with self.assertRaisesRegex(ValueError, "unsafe_entry"):
                inventory(path)
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("a", "file")
                z.writestr("a/b", "child")
            with self.assertRaisesRegex(ValueError, "conflicting_paths"):
                inventory(path)

    def test_missing_file_and_untrusted_archive_never_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected, active, output = (root / n for n in ("expected.zip", "active.zip", "report.json"))
            for path, names in ((expected, ("a", "b")), (active, ("a",))):
                with zipfile.ZipFile(path, "w") as z:
                    for name in names:
                        z.writestr(name, "value")
            digest = hashlib.sha256(expected.read_bytes()).hexdigest()
            self.assertEqual(compare_packages(expected, active, digest, output)["missingFiles"], 1)
            with self.assertRaisesRegex(ValueError, "archive_changed"):
                compare_packages(expected, active, "0" * 64, output)

    def test_unsafe_entries_rejected_without_extraction(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.zip"
            for name in ("../escape", "/absolute", "a\\b", "a/./b", "C:bad"):
                with zipfile.ZipFile(path, "w") as z:
                    z.writestr(name.replace("\\", "/"), "data")
                if "\\" in name:
                    # ZipInfo normalizes separators on Windows when writing.
                    path.write_bytes(path.read_bytes().replace(b"a/b", b"a\\b"))
                with self.assertRaisesRegex(ValueError, "unsafe_entry"):
                    inventory(path)


if __name__ == "__main__":
    unittest.main()
