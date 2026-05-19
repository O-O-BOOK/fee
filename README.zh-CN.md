# fee

`fee` 是一个面向 RT-Thread 的固定逻辑块 Flash EEPROM Emulation
（FEE）软件包。它面向可预测的块存储场景，强调分阶段启动恢复、后台 GC
和逻辑块级别的数据管理，而不是通用 KV 数据库接口。

## 软件包目录

- `src/`：FEE 核心实现和内部头文件
- `inc/`：对外公开头文件
- `port/`：默认弱符号 flash 适配层和 RAM mock 后端
- `samples/`：可选的 MSH 冒烟/诊断示例
- `docs/`：中英文设计与使用文档
- `package-index/`：单独保存的 Env 软件包索引材料

## 关键文件

- 对外 API：[inc/fee_api.h](./inc/fee_api.h)
- block/lane 配置：[inc/fee_cfg.h](./inc/fee_cfg.h)、
  [src/fee_cfg.c](./src/fee_cfg.c)
- 默认端口层：[inc/fee_port.h](./inc/fee_port.h)、
  [inc/fee_flash_drv.h](./inc/fee_flash_drv.h)、
  [port/fee_port.c](./port/fee_port.c)
- 可选示例：[samples/sample_fee.c](./samples/sample_fee.c)
- 构建接入：[Kconfig](./Kconfig)、[SConscript](./SConscript)
- 源仓库元数据：[package.json](./package.json)

## 功能摘要

- 基于 `block_id` 的逻辑块访问
- 同步读，异步排队的写入、失效、回滚
- 当前副本/上一副本并存，支持回滚和容错恢复
- 初始化完成后优先命中 RAM cache
- 基于 checkpoint 的分阶段启动恢复
- `FAST` / `NORMAL` / `BULK` lane 隔离
- 通过 `fee_mainfunction()` 推进后台 GC 和 checkpoint

## 文档入口

- 文档总索引：[docs/README.md](./docs/README.md)
- 中文文档：[docs/zh/README.md](./docs/zh/README.md)
- 英文文档：[docs/en/README.md](./docs/en/README.md)
- 对外 API 指南：[docs/zh/fee_API.md](./docs/zh/fee_API.md)
- 软件包集成步骤：[docs/zh/fee_package_integration.md](./docs/zh/fee_package_integration.md)

## 软件包索引提交

仓库中的 [package-index](./package-index) 是单独整理好的 Env 软件包索引目录，
用于提交到 `RT-Thread/packages` 的 `tools/fee` 路径，和源码仓库本身的
构建目录是分开的。
