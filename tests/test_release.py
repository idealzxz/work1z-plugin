"""Release/update integration tests; all installs and downloads are isolated."""
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import zipfile

from scripts import release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self.source.mkdir()
        for name in release.REQUIRED:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture: " + name, encoding="utf-8")
        self.set_version("0.1.0")
        self.old = self.make_package("0.1.0")
        self.installed = self.base / "installed"
        self.installed.mkdir()
        for name, data in self.old.items():
            path = self.installed / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.baseline = release.read_manifest(self.old[release.MANIFEST], "0.1.0")
        self.set_version("0.1.1")
        self.new = self.make_package("0.1.1")
        self.metadata = {
            "tag_name": "v0.1.1", "draft": False, "prerelease": False,
            "assets": [{"name": name, "browser_download_url":
                        "https://github.com/" + release.REPOSITORY + "/releases/download/v0.1.1/" + name}
                       for name in ("work1z-plugin-v0.1.1.zip", "work1z-plugin-v0.1.1.zip.sha256")],
        }

    def set_version(self, value):
        for name in release.CONFIGS:
            (self.source / name).write_text(json.dumps({"name": "work1z", "version": value}))

    def make_package(self, value):
        result = release.build(self.source, self.base / ("dist-" + value), "v" + value)
        return release.unpack(Path(result["archive"]).read_bytes(), value)

    def fake_fetch(self, url, limit=release.LIMIT):
        if url == release.API + "latest":
            return json.dumps(self.metadata).encode()
        if url == release.API + "tags/v0.1.0":
            old_meta = json.loads(json.dumps(self.metadata).replace("0.1.1", "0.1.0"))
            return json.dumps(old_meta).encode()
        for value in ("0.1.0", "0.1.1"):
            name = url.rsplit("/", 1)[-1]
            file = self.base / ("dist-" + value) / name
            if file.is_file():
                return file.read_bytes()
        raise AssertionError("Unexpected URL: " + url)

    def snapshot(self):
        return {p.relative_to(self.installed).as_posix(): p.read_bytes()
                for p in self.installed.rglob("*") if p.is_file()}

    def test_pack_excludes_junk_and_is_reproducible(self):
        (self.source / "skills/.DS_Store").write_text("junk")
        (self.source / "scripts/__pycache__").mkdir()
        (self.source / "scripts/__pycache__/x.pyc").write_bytes(b"junk")
        first = release.build(self.source, self.base / "one", "v0.1.1")
        second = release.build(self.source, self.base / "two", "v0.1.1")
        data = Path(first["archive"]).read_bytes()
        self.assertEqual(data, Path(second["archive"]).read_bytes())
        self.assertEqual(hashlib.sha256(data).hexdigest(), Path(first["checksum"]).read_text().split()[0])
        self.assertNotIn("skills/.DS_Store", release.unpack(data, "0.1.1"))

    def test_pack_rejects_version_mismatch(self):
        with self.assertRaisesRegex(ValueError, "Tag"):
            release.build(self.source, self.base / "out", "v9.0.0")
        (self.source / release.CONFIGS[1]).write_text('{"name":"work1z","version":"0.2.0"}')
        with self.assertRaisesRegex(ValueError, "versions"):
            release.build(self.source, self.base / "out", "v0.1.1")

    def test_update_end_to_end_preserves_extra_files(self):
        (self.installed / "local-note.txt").write_text("keep")
        with patch.object(release, "fetch", side_effect=self.fake_fetch):
            result = release.update(self.installed)
        self.assertEqual(result["status"], "updated")
        self.assertEqual((self.installed / "plugin.json").read_bytes(), self.new["plugin.json"])
        self.assertEqual((self.installed / "local-note.txt").read_text(), "keep")
        self.assertFalse((self.installed / ".work1z-update.lock").exists())
        self.assertEqual(release.read_manifest((self.installed / release.MANIFEST).read_bytes(), "0.1.1"),
                         release.read_manifest(self.new[release.MANIFEST], "0.1.1"))

    def test_cache_without_manifest_uses_published_baseline(self):
        (self.installed / release.MANIFEST).unlink()
        with patch.object(release, "fetch", side_effect=self.fake_fetch):
            self.assertEqual(release.update(self.installed)["status"], "updated")

    def test_local_edits_are_preserved(self):
        (self.installed / "skills/work1z/SKILL.md").write_text("my changes")
        before = self.snapshot()
        with patch.object(release, "fetch", side_effect=self.fake_fetch):
            with self.assertRaisesRegex(ValueError, "Local modification"):
                release.update(self.installed)
        self.assertEqual(self.snapshot(), before)

    def test_new_file_collision_is_preserved(self):
        (self.installed / "skills/custom.md").write_text("mine")
        payload = dict(self.new, **{"skills/custom.md": b"release"})
        with self.assertRaisesRegex(ValueError, "conflicts"):
            release.install(self.installed, payload, self.baseline)
        self.assertEqual((self.installed / "skills/custom.md").read_text(), "mine")

    def test_removed_release_files_are_removed(self):
        (self.installed / "skills/obsolete.md").write_bytes(b"old")
        baseline = dict(self.baseline, **{"skills/obsolete.md": release.digest(b"old")})
        release.install(self.installed, self.new, baseline)
        self.assertFalse((self.installed / "skills/obsolete.md").exists())

    def test_write_failure_rolls_back(self):
        before = self.snapshot()
        real_replace = release.os.replace
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated write failure")
            return real_replace(source, target)

        with patch.object(release.os, "replace", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "simulated"):
                release.install(self.installed, self.new, self.baseline)
        self.assertEqual(self.snapshot(), before)

    def test_no_release_and_network_error_are_distinct(self):
        with patch.object(release, "fetch", side_effect=urllib.error.HTTPError("url", 404, "not found", {}, None)):
            self.assertEqual(release.update(self.installed)["status"], "no_release")
        with patch.object(release, "fetch", side_effect=urllib.error.URLError("offline")):
            with self.assertRaises(urllib.error.URLError):
                release.update(self.installed)
        self.assertEqual(self.snapshot(), self.old)

    def test_does_not_downgrade_or_install_prerelease(self):
        for tag, prerelease, expected in (
            ("v0.1.0", False, "up_to_date"), ("v0.0.9", False, "up_to_date"),
            ("v0.2.0-rc.1", True, "no_stable_release"),
        ):
            self.metadata.update(tag_name=tag, prerelease=prerelease)
            with patch.object(release, "fetch", side_effect=self.fake_fetch):
                self.assertEqual(release.update(self.installed)["status"], expected)
        self.assertEqual(self.snapshot(), self.old)
        self.assertGreater(release.version("0.10.0"), release.version("0.9.0"))

    def test_check_only_and_git_checkout_do_not_write(self):
        with patch.object(release, "fetch", side_effect=self.fake_fetch):
            self.assertEqual(release.update(self.installed, True)["status"], "update_available")
            (self.installed / ".git").mkdir()
            self.assertEqual(release.update(self.installed)["status"], "source_checkout")
        self.assertEqual(self.snapshot(), self.old)

    def test_busy_update_does_not_write(self):
        (self.installed / ".work1z-update.lock").mkdir()
        with patch.object(release, "fetch", side_effect=self.fake_fetch):
            self.assertEqual(release.update(self.installed)["status"], "update_busy")
        self.assertEqual(self.snapshot(), self.old)

    def test_corrupt_download_does_not_write(self):
        before = self.snapshot()
        archive = self.base / "dist-0.1.1/work1z-plugin-v0.1.1.zip"
        archive.write_bytes(b"corrupt")
        with patch.object(release, "fetch", side_effect=self.fake_fetch):
            with self.assertRaisesRegex(ValueError, "Archive checksum"):
                release.update(self.installed)
        self.assertEqual(self.snapshot(), before)

    def test_unsafe_archive_is_rejected(self):
        for name in ("../outside", "/absolute", "skills/../../outside", "skills\\outside"):
            data = io.BytesIO()
            with zipfile.ZipFile(data, "w") as archive:
                archive.writestr("work1z-plugin/" + name, "bad")
            with self.assertRaises(ValueError):
                release.unpack(data.getvalue(), "0.1.1")

    def test_symlink_cannot_escape_installation(self):
        external = self.base / "external"
        external.write_text("keep")
        target = self.installed / "skills/work1z/SKILL.md"
        target.unlink()
        target.symlink_to(external)
        with self.assertRaisesRegex(ValueError, "symlink"):
            release.install(self.installed, self.new, self.baseline)
        self.assertEqual(external.read_text(), "keep")

    def test_rollback_failure_keeps_backup(self):
        real_replace = release.os.replace
        real_copy = release.shutil.copy2
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("write failure")
            return real_replace(source, target)

        def fail_restore(source, target):
            if "backup" in Path(source).parts:
                raise OSError("restore failure")
            return real_copy(source, target)

        with patch.object(release.os, "replace", side_effect=fail_second):
            with patch.object(release.shutil, "copy2", side_effect=fail_restore):
                with patch.object(release, "fetch", side_effect=self.fake_fetch):
                    with self.assertRaisesRegex(release.RecoveryRequired, "Rollback failed"):
                        release.update(self.installed)
        self.assertTrue((self.installed / ".work1z-update.lock").is_dir())
        backups = list(self.base.glob("work1z-update-*/backup/plugin.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), self.old["plugin.json"])

    def test_missing_assets_leave_installation_untouched(self):
        self.metadata["assets"] = []
        with patch.object(release, "fetch", side_effect=self.fake_fetch):
            with self.assertRaisesRegex(ValueError, "Missing release asset"):
                release.update(self.installed)
        self.assertEqual(self.snapshot(), self.old)

    def test_modified_zip_file_is_rejected_by_inventory(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as archive:
            for name, content in self.new.items():
                archive.writestr("work1z-plugin/" + name,
                                 b"tampered" if name == "skills/work1z/SKILL.md" else content)
        with self.assertRaisesRegex(ValueError, "file checksum"):
            release.unpack(data.getvalue(), "0.1.1")


if __name__ == "__main__":
    unittest.main()
