#!/usr/bin/env python3
"""Build SHA256SUMS.txt and latest.json from the assets of a release.

Usage:
  build_metadata.py --assets-dir assets --tag v0.1.0 --repo OWNER/REPO \
      --out-dir out [--published-at 2026-10-08T12:00:00Z]

Only .zip and .msi files are listed. Output:
  out/SHA256SUMS.txt  one "<sha256>  <name>" line per file (sha256sum format)
  out/latest.json     metadata read by the website
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
KINDS = {".zip": "zip", ".msi": "msi"}


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--published-at", default=None)
    args = parser.parse_args()

    version = args.tag[1:] if args.tag.startswith("v") else args.tag
    if not SEMVER.match(version):
        print(f"error: tag '{args.tag}' is not a version like v1.2.3", file=sys.stderr)
        return 1
    if not re.match(r"^[\w.-]+/[\w.-]+$", args.repo):
        print(f"error: repo '{args.repo}' is not OWNER/REPO", file=sys.stderr)
        return 1

    assets = sorted(
        p for p in Path(args.assets_dir).iterdir() if p.is_file() and p.suffix.lower() in KINDS
    )
    if not assets:
        print("error: no .zip or .msi assets found", file=sys.stderr)
        return 1

    base = f"https://github.com/{args.repo}/releases/download/{quote(args.tag)}"
    files = []
    for asset in assets:
        files.append(
            {
                "name": asset.name,
                "type": KINDS[asset.suffix.lower()],
                "size": asset.stat().st_size,
                "sha256": sha256_of(asset),
                "url": f"{base}/{quote(asset.name)}",
            }
        )

    published = args.published_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    latest = {
        "schema": 1,
        "version": version,
        "tag": args.tag,
        "published_at": published,
        "release_url": f"https://github.com/{args.repo}/releases/tag/{quote(args.tag)}",
        "files": files,
    }

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "SHA256SUMS.txt").write_text(
        "".join(f"{f['sha256']}  {f['name']}\n" for f in files), encoding="utf-8", newline="\n"
    )
    (out / "latest.json").write_text(
        json.dumps(latest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"ok: {len(files)} file(s) for {args.tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
