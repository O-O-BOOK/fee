# fee Package Index

This directory keeps a standalone Env package-index payload for `fee`.

## Layout

- `packages/Kconfig`: mini online-package root used for local verification
- `packages/tools/Kconfig`: `tools` category root for this package set
- `packages/tools/fee/`: package index files to submit upstream
- `env-verify/`: optional local Env verification workspace

## Upstream submission target

Submit or copy the following files to `RT-Thread/packages`:

- `packages/tools/fee/Kconfig`
- `packages/tools/fee/package.json`

When integrating into the upstream `tools` category, add:

```kconfig
source "$PKGS_DIR/packages/tools/fee/Kconfig"
```

to the upstream `packages/tools/Kconfig`.
