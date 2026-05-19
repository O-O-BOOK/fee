# fee 软件包集成步骤

本文档说明如何把 `fee` 作为 RT-Thread 在线软件包接入工程，并复现已经验证通过的下载、编译和运行流程。

## 1. 适用范围

本文覆盖两类集成场景：

1. 维护者把 `fee` 软件包索引提交到 `RT-Thread/packages`
2. BSP 或应用工程使用 Env 下载 `fee` 并完成编译验证

当前已经实际验证通过的环境如下：

- `fee` 源码仓库：`https://github.com/O-O-BOOK/fee`
- 软件包索引仓库：`https://github.com/O-O-BOOK/packages`
- 验证 BSP：`C:\sourcedata\rt-thread\bsp\qemu-vexpress-a9`
- 本地 Env：`C:\Work\InstallTools\env-windows`

## 2. 软件包索引准备

`fee` 源码仓库内已经单独维护了一份可提交的 Env 软件包索引，目录如下：

```text
package-index/
`-- packages/
    |-- Kconfig
    `-- tools/
        |-- Kconfig
        `-- fee/
            |-- Kconfig
            `-- package.json
```

其中真正需要提交到 `RT-Thread/packages` 的文件只有两个：

- `package-index/packages/tools/fee/Kconfig`
- `package-index/packages/tools/fee/package.json`

同时需要在 `RT-Thread/packages/tools/Kconfig` 中增加一行：

```kconfig
source "$PKGS_DIR/packages/tools/fee/Kconfig"
```

## 3. 向 RT-Thread/packages 提交

如果要把本仓库内容提交到 `RT-Thread/packages`，建议按下面步骤处理：

1. Fork `https://github.com/RT-Thread/packages`
2. 把 `package-index/packages/tools/fee/` 复制到 fork 仓库的 `tools/fee/`
3. 修改 fork 仓库的 `tools/Kconfig`，加入 `fee` 的 `source`
4. 提交并推送到自己的 fork
5. 从自己的 fork 向 `RT-Thread/packages` 发起 PR

本次整理后的对应位置如下：

- `tools/fee/Kconfig`
- `tools/fee/package.json`
- `tools/Kconfig`

## 4. BSP 侧接入前提

目标 BSP 需要允许在线软件包的 `Kconfig` 被纳入菜单。

以 `qemu-vexpress-a9` 为例，BSP 根目录 `Kconfig` 中需要有：

```kconfig
PKGS_DIR := packages
osource "$PKGS_DIR/Kconfig"
```

如果 BSP 本地没有 `packages/Kconfig` 桥接文件，需要补一个最小文件：

```kconfig
source "$PKGS_DIR/packages/Kconfig"
```

说明：

- 这个桥接文件位于 BSP 本地 `packages/Kconfig`
- 其作用是把 Env 生成的 `packages/packages/Kconfig` 接到 BSP 菜单中
- 某些 BSP 已经自带该文件，则不需要重复添加

## 5. 使用本地 package-index 验证

在 `fee` 还没有合入 `RT-Thread/packages` 主仓库之前，可以直接使用源码仓库里的 `package-index/` 做本地验证。

### 5.1 进入 BSP 目录

```cmd
cd /d C:\sourcedata\rt-thread\bsp\qemu-vexpress-a9
call C:\Work\InstallTools\env-windows\tools\bin\env-init.bat
```

### 5.2 指向本地 package-index

```cmd
set PKGS_ROOT=C:\sourcedata\custom_fee\package-index
set PKGS_DIR=%PKGS_ROOT%
```

说明：

- `PKGS_ROOT` 指向独立的软件包索引根目录
- `PKGS_DIR` 同步设置为相同路径，便于 Env 按该索引解析包信息

### 5.3 打开 menuconfig 使能软件包

```cmd
menuconfig
```

建议在菜单中完成以下配置：

1. 关闭旧的本地组件接入方式，例如 `COMPONENT_USING_CUSTOM_FEE`
2. 进入 `RT-Thread online packages -> tools packages`
3. 使能 `fee`
4. 版本选择优先使用 `latest`
5. 按需打开 `Enable samples`
6. 按需设置 `RAM mock flash size`，本次验证使用 `0xA0000`

本次实际验证对应的关键配置为：

```config
CONFIG_PKG_USING_FEE=y
CONFIG_PKG_FEE_PATH="/packages/tools/fee"
CONFIG_FEE_MOCK_FLASH_SIZE=0xA0000
CONFIG_FEE_USING_SAMPLE=y
CONFIG_PKG_USING_FEE_LATEST_VERSION=y
CONFIG_PKG_FEE_VER="latest"
```

### 5.4 下载软件包

```cmd
pkgs --update
```

正常情况下会把软件包下载到 BSP 本地目录：

```text
packages\fee-latest
```

### 5.5 编译 BSP

```cmd
scons -j8
```

本次验证时，构建日志已经确认编译输入来自：

```text
build\packages\fee-latest\...
```

这说明参与构建的是 Env 下载的软件包，而不是旧的本地源码副本。

## 6. 运行验证

以 `qemu-vexpress-a9` 为例，可以启动 QEMU 后在 MSH 中执行示例命令：

```text
fee_test
fee_diag_test
```

本次验证通过时的关键输出为：

```text
fee_test: start
fee_test: PASS
fee_diag_test: PASS
```

如果工程没有打开 `FEE_USING_SAMPLE`，则不会导出这两个命令。

## 7. 合入主仓库后的常规使用

当 `fee` 已经合入 `RT-Thread/packages` 后，普通使用者不需要再手动设置本地 `PKGS_ROOT`。

常规流程如下：

1. 在 BSP 目录执行 `env` 初始化
2. 运行 `menuconfig`
3. 在在线软件包菜单中使能 `fee`
4. 执行 `pkgs --update`
5. 执行 `scons -j8`

如果 BSP 的 `packages/Kconfig` 桥接尚未准备好，仍然需要先补齐第 4 节中的桥接文件。

## 8. 已知限制

当前 Env 对 git 软件包固定 tag 版本的处理存在一个兼容性问题：

1. `pkgs --update` 会先执行浅克隆
2. 然后再执行 `git checkout <VER_SHA>`
3. 当 `VER_SHA` 是 tag，例如 `v0.1.0` 时，浅克隆结果里可能没有对应 tag
4. 最终表现为 `git checkout v0.1.0` 失败

因此：

- `latest` 已经完成实际下载、编译、运行验证
- `v0.1.0` 的元数据仍然保留，便于软件包索引按规范提供固定版本
- 如果当前本地 Env 直接选择 `v0.1.0`，可能会因浅克隆未带 tag 而失败

在 Env 修复该行为前，建议本地联调优先使用 `latest`。

## 9. 仓库内相关文件

和软件包接入直接相关的文件如下：

- `Kconfig`
- `SConscript`
- `package.json`
- `samples/sample_fee.c`
- `package-index/packages/tools/fee/Kconfig`
- `package-index/packages/tools/fee/package.json`
- `tools/verify_package_layout.py`
- `tools/verify_env_package_index.py`

建议维护者在修改包结构或索引后，至少重新执行一次：

```cmd
python tools\verify_package_layout.py
python tools\verify_env_package_index.py
```
