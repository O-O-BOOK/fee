# fee

`fee` is a fixed-block Flash EEPROM emulation package for RT-Thread. It
focuses on deterministic logical-block storage, staged boot recovery, and
background garbage collection instead of a general-purpose KV interface.

## Package layout

- `src/`: core FEE implementation and internal headers
- `inc/`: public headers exposed to applications and adapters
- `port/`: default weak flash-driver adapter and RAM-backed mock backend
- `samples/`: optional MSH-based smoke and diagnostic sample
- `docs/`: English and Chinese design and usage documents
- `package-index/`: separate Env package-index payload for `RT-Thread/packages`

## Key files

- Public API: [inc/fee_api.h](./inc/fee_api.h)
- Block and lane configuration: [inc/fee_cfg.h](./inc/fee_cfg.h),
  [src/fee_cfg.c](./src/fee_cfg.c)
- Default port layer: [inc/fee_port.h](./inc/fee_port.h),
  [inc/fee_flash_drv.h](./inc/fee_flash_drv.h),
  [port/fee_port.c](./port/fee_port.c)
- Optional sample: [samples/sample_fee.c](./samples/sample_fee.c)
- Build integration: [Kconfig](./Kconfig), [SConscript](./SConscript)
- Source metadata: [package.json](./package.json)

## Functional summary

- Block-oriented access by `block_id`
- Synchronous reads plus queued write, invalidate, and rollback jobs
- Current/previous copy tracking for rollback and tolerant recovery
- RAM cache lookups after initialization
- Checkpoint-assisted staged startup recovery
- Lane separation for fast, normal, and bulk traffic
- Background GC and checkpoint advancement in `fee_mainfunction()`

## Documentation

- Documentation index: [docs/README.md](./docs/README.md)
- English set: [docs/en/README.md](./docs/en/README.md)
- Chinese set: [docs/zh/README.md](./docs/zh/README.md)
- Public API guide: [docs/en/fee_API.md](./docs/en/fee_API.md)

## Package index submission

The repository also includes a standalone Env package-index mirror under
[package-index](./package-index). That directory is meant to be copied or
submitted to the `tools/fee` path of `RT-Thread/packages`; it is not
used by the source build itself.

