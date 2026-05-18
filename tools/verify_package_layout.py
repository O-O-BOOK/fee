from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_DIRS = [
    "src",
    "inc",
    "samples",
    "docs",
    "docs/en",
    "docs/zh",
    "port",
    "package-index",
    "package-index/packages",
    "package-index/packages/tools",
]

REQUIRED_FILES = [
    "SConscript",
    "Kconfig",
    "package.json",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "inc/fee_api.h",
    "inc/fee_cfg.h",
    "inc/fee_port.h",
    "inc/fee_flash_drv.h",
    "src/fee_api.c",
    "src/SConscript",
    "samples/sample_fee.c",
    "samples/SConscript",
    "port/fee_port.c",
    "port/SConscript",
    "docs/README.md",
    "docs/en/README.md",
    "docs/zh/README.md",
    "package-index/README.md",
    "package-index/packages/Kconfig",
    "package-index/packages/tools/Kconfig",
    "package-index/packages/tools/fee/Kconfig",
    "package-index/packages/tools/fee/package.json",
]


def main() -> int:
    missing: list[str] = []

    for rel in REQUIRED_DIRS:
        path = ROOT / rel
        if not path.is_dir():
            missing.append(f"missing dir: {rel}")

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.is_file():
            missing.append(f"missing file: {rel}")

    if missing:
        print("package layout verification failed:")
        for item in missing:
            print(f"  - {item}")
        return 1

    print("package layout verification passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
