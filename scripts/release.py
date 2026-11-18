#!/usr/bin/env python3
"""Build and update Work1z release packages. Python 3.9+, standard library only."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import urllib.error
import urllib.request
import zipfile

REPOSITORY = "idealzxz/work1z-plugin"
API = "https://api.github.com/repos/" + REPOSITORY + "/releases/"
MANIFEST = ".work1z-release.json"
ROOT = Path(__file__).resolve().parents[1]
CONFIGS = ("plugin.json", ".claude-plugin/plugin.json", ".qoder-plugin/plugin.json")
DIRECTORIES = ("skills", "assets", "scripts", ".agents", ".claude-plugin", ".qoder-plugin")
REQUIRED = CONFIGS + (
    "README.md", "README.en.md", ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json", "skills/work1z/SKILL.md",
    "skills/humanizer-zh/SKILL.md", "skills/humanizer-zh/LICENSE",
    "skills/work1z/scripts/validate_docs.py", "scripts/release.py",
)
LIMIT = 64 * 1024 * 1024


class RecoveryRequired(OSError):
    """An incomplete rollback requires manual recovery before further use."""


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value):
        raise ValueError("Expected a stable MAJOR.MINOR.PATCH version")
    return tuple(int(part) for part in value.split("."))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(name):
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or "\\" in name or ":" in name
            or any(part in ("", ".", "..") for part in name.split("/"))):
        raise ValueError("Unsafe package path: " + name)
    if name not in ("plugin.json", "README.md", "README.en.md", MANIFEST) and path.parts[0] not in DIRECTORIES:
        raise ValueError("Unexpected package path: " + name)
    if any(part in (".git", ".DS_Store", "__pycache__") for part in path.parts) or name.endswith(".pyc"):
        raise ValueError("Excluded package path: " + name)
    return path


def validate_payload(payload, expected=None):
    for name in REQUIRED:
        if name not in payload:
            raise ValueError("Missing required file: " + name)
    versions = []
    for name in CONFIGS:
        config = json.loads(payload[name])
        if config.get("name") != "work1z":
            raise ValueError("Wrong plugin identity: " + name)
        version(config["version"])
        versions.append(config["version"])
    if len(set(versions)) != 1 or (expected is not None and versions[0] != expected):
        raise ValueError("Plugin manifest versions must match the release tag")
    return versions[0]


def collect(root):
    payload = {}
    candidates = [root / name for name in ("plugin.json", "README.md", "README.en.md")]
    for directory in DIRECTORIES:
        candidates.extend((root / directory).rglob("*"))
    for path in sorted(candidates):
        if any(part in (".DS_Store", "__pycache__") for part in path.parts) or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError("Package cannot contain symlinks: " + str(path))
        if path.is_file():
            name = path.relative_to(root).as_posix()
            safe_path(name)
            payload[name] = path.read_bytes()
    return payload


def build(root, output, tag):
    payload = collect(root)
    current = validate_payload(payload)
    if tag != "v" + current:
        raise ValueError("Tag must equal v" + current)
    metadata = {"repository": REPOSITORY, "version": current,
                "files": {name: digest(data) for name, data in payload.items()}}
    payload[MANIFEST] = (json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / ("work1z-plugin-" + tag + ".zip")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo("work1z-plugin/" + name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            package.writestr(info, data)
    checksum = archive.with_suffix(".zip.sha256")
    checksum.write_text(digest(archive.read_bytes()) + "  " + archive.name + "\n", encoding="utf-8")
    return {"status": "packaged", "version": current, "archive": str(archive), "checksum": str(checksum)}


def read_manifest(data, expected):
    manifest = json.loads(data)
    if manifest.get("repository") != REPOSITORY or manifest.get("version") != expected:
        raise ValueError("Release manifest identity/version mismatch")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files or MANIFEST in files:
        raise ValueError("Invalid release file inventory")
    for name, checksum in files.items():
        safe_path(name)
        if not isinstance(checksum, str) or not re.fullmatch("[0-9a-f]{64}", checksum):
            raise ValueError("Invalid file checksum")
    if not set(REQUIRED).issubset(files):
        raise ValueError("Incomplete release file inventory")
    return files


def unpack(data, expected):
    payload = {}
    total = 0
    with zipfile.ZipFile(io.BytesIO(data)) as package:
        for info in package.infolist():
            if not info.filename.startswith("work1z-plugin/") or info.is_dir():
                raise ValueError("Unexpected ZIP layout")
            name = info.filename[len("work1z-plugin/"):]
            safe_path(name)
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode) or name in payload:
                raise ValueError("Symlink or duplicate ZIP entry")
            total += info.file_size
            if total > LIMIT:
                raise ValueError("Unpacked release exceeds size limit")
            payload[name] = package.read(info)
    validate_payload(payload, expected)
    inventory = read_manifest(payload[MANIFEST], expected)
    if set(payload) != set(inventory) | {MANIFEST}:
        raise ValueError("ZIP contents differ from file inventory")
    if any(digest(payload[name]) != checksum for name, checksum in inventory.items()):
        raise ValueError("Release file checksum mismatch")
    return payload


def fetch(url, limit=LIMIT):
    request = urllib.request.Request(url, headers={
        "User-Agent": "work1z-release-updater", "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Download exceeds size limit")
    return data


def release_package(release):
    tag = release["tag_name"]
    if not tag.startswith("v"):
        raise ValueError("Release tag must start with v")
    current = tag[1:]
    version(current)
    if release.get("draft") or release.get("prerelease"):
        raise ValueError("Only published stable releases are supported")
    name = "work1z-plugin-" + tag + ".zip"
    assets = {item["name"]: item["browser_download_url"] for item in release["assets"]}
    prefix = "https://github.com/" + REPOSITORY + "/releases/download/" + tag + "/"
    for asset in (name, name + ".sha256"):
        if assets.get(asset) != prefix + asset:
            raise ValueError("Missing release asset or unexpected download URL: " + asset)
    checksum = fetch(assets[name + ".sha256"], 4096).decode().strip().split()
    if len(checksum) != 2 or checksum[1] != name:
        raise ValueError("Invalid archive checksum file")
    data = fetch(assets[name])
    if digest(data) != checksum[0]:
        raise ValueError("Archive checksum mismatch")
    return unpack(data, current)


def local_path(root, name):
    safe_path(name)
    target = root / name
    for path in (target, *target.parents):
        if path == root:
            break
        if path.is_symlink():
            raise ValueError("Local symlink would be overwritten: " + name)
    return target


def check_local(root, baseline, incoming):
    for name, checksum in baseline.items():
        path = local_path(root, name)
        if not path.is_file() or digest(path.read_bytes()) != checksum:
            raise ValueError("Local modification detected; update skipped: " + name)
    for name in set(incoming) - set(baseline) - {MANIFEST}:
        if local_path(root, name).exists():
            raise ValueError("New release conflicts with local file: " + name)
    local_path(root, MANIFEST)


def install(root, payload, baseline):
    check_local(root, baseline, payload)
    # Prepare all writes and backups before touching installed files.
    names = sorted((set(baseline) | set(payload)) - {MANIFEST}) + [MANIFEST]
    workspace = Path(tempfile.mkdtemp(prefix="work1z-update-", dir=root.parent))
    stage = workspace / "stage"
    backup = workspace / "backup"
    keep_backup = False
    try:
        originals = set()
        for name in names:
            target = local_path(root, name)
            if target.exists():
                saved = backup / name
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, saved)
                originals.add(name)
            if name in payload:
                replacement = stage / name
                replacement.parent.mkdir(parents=True, exist_ok=True)
                replacement.write_bytes(payload[name])
        check_local(root, baseline, payload)
        changed = []
        try:
            for name in names:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if name in payload:
                    os.replace(stage / name, target)
                else:
                    target.unlink()
                changed.append(name)
        except OSError as write_error:
            try:
                for name in reversed(changed):
                    target = root / name
                    if name in originals:
                        shutil.copy2(backup / name, target)
                    elif target.exists():
                        target.unlink()
            except OSError as rollback_error:
                keep_backup = True
                raise RecoveryRequired("Rollback failed; stop using the plugin. Backup preserved at "
                              + str(backup) + ": " + str(rollback_error)) from write_error
            raise OSError("Update failed and was rolled back: " + str(write_error)) from write_error
    finally:
        if not keep_backup:
            shutil.rmtree(workspace)


def update(root, check_only=False):
    current = json.loads((root / "plugin.json").read_text(encoding="utf-8"))["version"]
    version(current)
    try:
        release = json.loads(fetch(API + "latest", 1024 * 1024))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return {"status": "no_release", "version": current}
        raise
    tag = release["tag_name"]
    if release.get("draft") or release.get("prerelease"):
        return {"status": "no_stable_release", "version": current}
    if not tag.startswith("v"):
        raise ValueError("Release tag must start with v")
    latest = tag[1:]
    if version(latest) <= version(current):
        return {"status": "up_to_date", "version": current, "latest": latest}
    result = {"version": current, "latest": latest}
    if check_only:
        return dict(result, status="update_available")
    if (root / ".git").exists():
        return dict(result, status="source_checkout", message="Update the development checkout manually")
    lock = root / ".work1z-update.lock"
    try:
        lock.mkdir()
    except FileExistsError:
        return dict(result, status="update_busy", message="Another update is running, or a stale lock needs review")
    recovery_required = False
    try:
        payload = release_package(release)
        manifest_path = local_path(root, MANIFEST)
        if manifest_path.exists():
            baseline = read_manifest(manifest_path.read_bytes(), current)
        else:
            # Host caches created from Git may omit the generated release inventory.
            previous = json.loads(fetch(API + "tags/v" + current, 1024 * 1024))
            previous_payload = release_package(previous)
            baseline = read_manifest(previous_payload[MANIFEST], current)
        install(root, payload, baseline)
        return dict(result, status="updated", version=latest, previous=current,
                    reload_required=True, message="Files updated; reload skill instructions before continuing")
    except RecoveryRequired:
        recovery_required = True
        raise
    finally:
        if not recovery_required:
            lock.rmdir()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    package = subcommands.add_parser("pack", help="Build ZIP and SHA-256 file")
    package.add_argument("--tag", required=True)
    package.add_argument("--output", type=Path, required=True)
    updater = subcommands.add_parser("update", help="Check the official stable release and update this installation")
    updater.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "pack":
            result = build(ROOT, args.output.resolve(), args.tag)
        else:
            result = update(ROOT, args.check_only)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
        print(json.dumps({"status": "error", "message": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
