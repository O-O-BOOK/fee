from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKGS_ROOT = ROOT / "package-index"
CONFIG_FILE = PKGS_ROOT / "env-verify" / ".config"


def parse_config(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key] = value.strip().strip('"')
    return result


def main() -> int:
    if not CONFIG_FILE.is_file():
        print(f"missing config: {CONFIG_FILE}")
        return 1

    cfg = parse_config(CONFIG_FILE)
    pkg_path = cfg.get("CONFIG_PKG_FEE_PATH")
    pkg_ver = cfg.get("CONFIG_PKG_FEE_VER")

    if pkg_path != "/packages/tools/fee":
        print(f"unexpected package path: {pkg_path!r}")
        return 1

    if pkg_ver != "v0.1.0":
        print(f"unexpected package version: {pkg_ver!r}")
        return 1

    package_json = PKGS_ROOT / pkg_path.lstrip("/") / "package.json"
    if not package_json.is_file():
        print(f"missing package index json: {package_json}")
        return 1

    package = json.loads(package_json.read_text(encoding="utf-8"))
    if package.get("category") != "tools":
        print(f"unexpected category: {package.get('category')!r}")
        return 1

    if package.get("name") != "fee":
        print(f"unexpected package name: {package.get('name')!r}")
        return 1

    if package.get("enable") != "PKG_USING_FEE":
        print(f"unexpected enable symbol: {package.get('enable')!r}")
        return 1

    site = package.get("site", [])
    versions = {entry.get("version"): entry for entry in site}
    if set(versions) != {"v0.1.0", "latest"}:
        print(f"unexpected site versions: {sorted(versions)}")
        return 1

    if versions["v0.1.0"].get("VER_SHA") != "v0.1.0":
        print(f"unexpected v0.1.0 VER_SHA: {versions['v0.1.0'].get('VER_SHA')!r}")
        return 1

    if versions["latest"].get("VER_SHA") != "main":
        print(f"unexpected latest VER_SHA: {versions['latest'].get('VER_SHA')!r}")
        return 1

    print("env package index verification passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
