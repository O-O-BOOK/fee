# fee Package Rework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure `fee` into an RT-Thread package-style source repository and add a separate `tools` package index payload compatible with Env.

**Architecture:** Keep the existing C implementation intact while reorganizing files into `src/inc/samples/docs/port`, updating build glue to package conventions, and generating a standalone `package-index/packages/tools/fee` tree for Env package indexing. Use a lightweight local verification script plus Env-based validation.

**Tech Stack:** C, RT-Thread `Kconfig`/`SConscript`, Python verification script, Env package index format

---

### Task 1: Add a failing repository layout check

**Files:**
- Create: `docs/superpowers/plans/2026-05-18-custom-fee-package-rework.md`
- Create: `tools/verify_package_layout.py`
- Create: `.gitignore`

- [ ] **Step 1: Write the failing layout test**

```python
REQUIRED_DIRS = ["src", "inc", "samples", "docs", "port", "package-index"]
REQUIRED_FILES = ["SConscript", "Kconfig", "README.md", "README.zh-CN.md", "LICENSE"]
```

- [ ] **Step 2: Run the layout test to verify it fails**

Run: `python tools/verify_package_layout.py`
Expected: FAIL with missing directories and files

- [ ] **Step 3: Add minimal verification scaffolding**

```python
if missing:
    print("package layout verification failed:")
    return 1
```

- [ ] **Step 4: Re-run to keep the expected failing baseline**

Run: `python tools/verify_package_layout.py`
Expected: FAIL

### Task 2: Reorganize the source tree and build scripts

**Files:**
- Modify: `SConscript`
- Modify: `Kconfig`
- Create: `src/SConscript`
- Create: `port/SConscript`
- Create: `samples/SConscript`
- Move: `fee_api.c` -> `src/fee_api.c`
- Move: `fee_cache.c` -> `src/fee_cache.c`
- Move: `fee_cfg.c` -> `src/fee_cfg.c`
- Move: `fee_ckpt.c` -> `src/fee_ckpt.c`
- Move: `fee_core.c` -> `src/fee_core.c`
- Move: `fee_gc.c` -> `src/fee_gc.c`
- Move: `fee_lane_bulk.c` -> `src/fee_lane_bulk.c`
- Move: `fee_lane_fast.c` -> `src/fee_lane_fast.c`
- Move: `fee_lane_log.c` -> `src/fee_lane_log.c`
- Move: `fee_onflash.c` -> `src/fee_onflash.c`
- Move: `fee_recovery.c` -> `src/fee_recovery.c`
- Move: `fee_sched.c` -> `src/fee_sched.c`
- Move: `fee_internal.h` -> `src/fee_internal.h`
- Move: `fee_onflash.h` -> `src/fee_onflash.h`
- Move: `fee_api.h` -> `inc/fee_api.h`
- Move: `fee_cfg.h` -> `inc/fee_cfg.h`
- Move: `fee_port.h` -> `inc/fee_port.h`
- Move: `fee_flash_drv.h` -> `inc/fee_flash_drv.h`
- Move: `fee_port.c` -> `port/fee_port.c`
- Move: `fee_test.c` -> `samples/sample_fee.c`

- [ ] **Step 1: Create package-style directories**

```text
src/
inc/
port/
samples/
docs/
package-index/
```

- [ ] **Step 2: Move implementation and header files into their package-style directories**

```text
src/*.c + src/internal headers
inc/public headers
port/fee_port.c
samples/sample_fee.c
```

- [ ] **Step 3: Replace the root bridge SConscript with package-style subdirectory dispatch**

```python
if GetDepend('PKG_USING_FEE'):
    objs += SConscript(os.path.join('src', 'SConscript'))
    objs += SConscript(os.path.join('port', 'SConscript'))
    if GetDepend('FEE_USING_SAMPLE'):
        objs += SConscript(os.path.join('samples', 'SConscript'))
```

- [ ] **Step 4: Replace the root Kconfig option with package naming**

```kconfig
menuconfig PKG_USING_FEE
    bool "fee: fixed-block Flash EEPROM emulation package"
```

- [ ] **Step 5: Add package-style subdirectory SConscript files**

```python
group = DefineGroup('fee', src, depend=['PKG_USING_FEE'], CPPPATH=[cwd, cwd + '/../inc'])
```

- [ ] **Step 6: Run the layout test and inspect remaining failures**

Run: `python tools/verify_package_layout.py`
Expected: still FAIL, but only for remaining docs/license/package-index gaps

### Task 3: Rewrite package metadata and user-facing docs

**Files:**
- Create: `LICENSE`
- Create: `package.json`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Create: `docs/README.md`
- Move: `doc/en/*` -> `docs/en/*`
- Move: `doc/zh/*` -> `docs/zh/*`
- Modify: `docs/en/README.md`
- Modify: `docs/zh/README.md`

- [ ] **Step 1: Add the Apache-2.0 license file**

```text
Apache License
Version 2.0, January 2004
```

- [ ] **Step 2: Add source-repository `package.json` metadata**

```json
{
  "name": "fee",
  "description": "Fixed-block Flash EEPROM emulation component for RT-Thread",
  "type": "rt-thread-component"
}
```

- [ ] **Step 3: Rewrite the English and Chinese root README files for the new structure**

```markdown
RT-Thread online packages -> tools packages -> fee
```

- [ ] **Step 4: Move `doc/` to `docs/` and add a new docs index**

```markdown
- docs/en/
- docs/zh/
```

- [ ] **Step 5: Update broken relative links that still point to the old root layout**

```text
../../fee_api.h -> ../../inc/fee_api.h
../../Kconfig -> ../../Kconfig
```

- [ ] **Step 6: Run the layout test again**

Run: `python tools/verify_package_layout.py`
Expected: FAIL only for missing `package-index` payload, if any

### Task 4: Add Env package index payload under `tools`

**Files:**
- Create: `package-index/README.md`
- Create: `package-index/packages/tools/fee/Kconfig`
- Create: `package-index/packages/tools/fee/package.json`

- [ ] **Step 1: Create an Env-style index mirror directory**

```text
package-index/packages/tools/fee/
```

- [ ] **Step 2: Add Env-style package Kconfig**

```kconfig
menuconfig PKG_USING_FEE
    bool "fee: fixed-block Flash EEPROM emulation package"
```

- [ ] **Step 3: Add Env-style package.json with `latest` as the validated version**

```json
{
  "name": "fee",
  "enable": "PKG_USING_FEE",
  "category": "tools"
}
```

- [ ] **Step 4: Document how to merge the package into `packages/tools/Kconfig`**

```markdown
source "$PKGS_DIR/packages/tools/fee/Kconfig"
```

- [ ] **Step 5: Run the layout test and confirm it passes**

Run: `python tools/verify_package_layout.py`
Expected: PASS

### Task 5: Validate with local Env-compatible checks

**Files:**
- Modify: `tools/verify_package_layout.py` if validation needs a small extension

- [ ] **Step 1: Re-run the repository layout verifier**

Run: `python tools/verify_package_layout.py`
Expected: `package layout verification passed`

- [ ] **Step 2: Validate JSON syntax for both package metadata files**

Run: `python -m json.tool package.json`
Expected: pretty-printed JSON, exit 0

Run: `python -m json.tool package-index/packages/tools/fee/package.json`
Expected: pretty-printed JSON, exit 0

- [ ] **Step 3: Verify Env tooling is reachable**

Run: `cmd /c "call C:\Work\InstallTools\env-windows\tools\bin\env-init.bat && pkgs --help"`
Expected: shows `pkgs` help and `--wizard`

- [ ] **Step 4: Inspect the resulting file tree**

Run: `rg --files`
Expected: includes `src/`, `inc/`, `port/`, `samples/`, `docs/`, and `package-index/packages/tools/fee/`
