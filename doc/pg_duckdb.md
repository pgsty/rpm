# pg_duckdb 1.2.0 候选构建

本轮打包 pg_duckdb 1.2.0 与其固定的 DuckDB 2.0.0，目标是
EL8/9/10 × x86_64/aarch64，以及 Debian 12/13、Ubuntu 22.04/24.04/26.04
× amd64/arm64，全部覆盖 PG14–18。共 80 个坐标，预期 90 个 RPM
（主包、debuginfo、debugsource）和 100 个 DEB（主包、dbgsym）。
SRPM、buildinfo、changes 和验收证据另行保存，不计入这 190 个二进制包。

上游将 [v1.2.0](https://github.com/duckdb/pg_duckdb/releases/tag/v1.2.0)
标为 Experimental。构建和隔离验收不改变这一定位。
本轮只收集候选，不进入生产 staging，不签名、发布或写入 PGEXT。

## 源码与依赖

| 输入 | 固定版本或提交 | SHA-256 |
| --- | --- | --- |
| `pg_duckdb-1.2.0.tar.gz` | pg_duckdb `8756099e267c47f0b86c24de4cf995327f1f4279`；DuckDB `d54cbbe3df17e8e5ce68312f483b4155836112aa` | `c2209ab8ac81b5d9f15be7dbca1a3ce42cded007a301498a8c90c7337952722f` |
| `curl-8.23.0.tar.gz` | [curl 8.23.0 官方源码](https://curl.se/download/curl-8.23.0.tar.gz) | `e3de77cfa6367083c776a26647fc9f633b538c06c3baa73d931a252ac8f72b49` |

归档保存在 `~/pgsty/repo/ext/src/`，主归档解包目录为
`pg_duckdb-1.2.0`，包含 DuckDB 源码和 `SOURCE_MANIFEST.json`。
它不是离线依赖全集：httpfs 仍由上游 CMake 获取固定提交
`77392a72077a85897db2519fae11e2c0da972b8a`，GitHub 请求经本机代理或其 SSH 转发。

builder 先运行 `pig build get pg_duckdb`；仅当取不到所需归档时，
复制缺失的具体文件。本轮未向 macOS 仓库的 `rpmbuild/SOURCES/` 写入源码。
系统 libcurl 低于 7.85 时，在构建树内生成私有 PIC 静态 curl，
供 httpfs 使用，不替换系统 libcurl。新增 curl 输入的 PGEXT 来源字段同步是外部待办。

## 打包修复

- RPM 与 DEB 共用源码补丁：按随包源码代替 Git 子模块初始化，保证安装目录顺序，
  并通过上游 `APPLY_PATCHES` 钩子修复 GCC 8–11 的 `unique_ptr` 返回转换。
- EL8 使用并行安装的 OpenSSL 3 头文件和库；其系统默认 OpenSSL 1.1 不满足 curl 8.23。
  DuckDB 2.0 需要 GCC 8 标准库缺失的 `reference_wrapper` 转换，因此使用 GCC Toolset 15
  及对应 annobin 插件。EL8 专用补丁只对支持该选项的 C++ 编译启用 httpfs 警告参数。
- 桥接库保留动态 `libduckdb.so` 依赖。EL10 安装时把桥接库 RUNPATH 设为 `$ORIGIN`，
  从同一 PG 主版本的私有目录加载核心，并通过 EL10 的 `check-rpaths`。
- PG18 在 PGXS 读取变量前传入 `PG_DUCKDB_VERSION`，确保
  `pg_get_loaded_modules()` 的模块版本为 `v1.2.0`，不能接受 `unknown`。
- DEB 禁用 DWZ 的跨文件合并，保留逐 ELF 的 DWARF 优化与 dbgsym；
  随后在 `dh_strip` 前，仅对安装暂存树中的 `libduckdb.so` 写入确定性的 PG 专属
  Build-ID。单独禁用跨文件合并仍不能解决多个 dbgsym 包共同拥有全局 Build-ID
  路径的问题。新 Build-ID 由该 ELF 的内容与 PG 主版本共同生成，缓存字节不变，
  自动分离的调试文件使用各 PG 独立的路径。

这些是源码构建、平台或包布局修复。没有补写上游 SQL 升级脚本或数据库迁移功能。
版本仍为 `1.2.0-1PGSTY`；构建重试和本地提交不是二进制发布。

## 构建与验收方法

DuckDB 内层固定两个任务。核心缓存仅在同平台、同架构内使用，key 包含
源码、补丁、commit、依赖版本、编译器和实际编译/链接参数。
PGXS 桥接层逐 PG 主版本重建。恢复匹配缓存后更新核心库时间戳，
避免相同补丁的新时间戳触发不必要的核心重新链接。

保留 LLVM，主包拥有全部 49 个 bitcode 文件及 index；不生成扩展级 llvmjit 子包，
主包不依赖 LLVM、Clang 或 PostgreSQL core 的 llvmjit 包。
桥接库保留发行版完整 `-g`，DuckDB 核心保留既有 `-g1` 的函数与行号 DWARF，
后者不包含完整变量调试信息。

每个坐标检查包身份、逐文件归属、上游 control/SQL 字节、bitcode 清单、
两个原生 ELF 的 Build-ID 与对应 DWARF，以及 59 项必需主包 payload 的安装后 SHA-256。
PG14–17 执行 27 项隔离运行检查；PG18 增加严格模块版本检查，共 28 项。
覆盖预加载、DuckDB 版本、执行计划、事务与回滚、跨连接读取、非 public 安装、
本地 JSON/Parquet、同批 httpfs 插件字节身份与真实本机 HTTP 读取。
每个平台在第二个 PG 和全部五个 PG 后检查主包与完整 debug 包族共装。

DEB dbgsym 以构建器实际生成的 `.deb` 或 `.ddeb` 文件名收集；不为统一后缀改名。
测试允许同批未签名 httpfs 插件，不表示公共插件、MotherDuck 或云认证集成通过。

## 证据与交付位置

实时台账、冻结输入、失败现场、命令双流、退出码、资源记录和最终回执位于：

```text
~/pgsty/artifacts/full-matrix-20261103/stage-b-pg-duckdb/
```

`status/targets.json` 区分逐坐标验收与收集状态；`status/control-state.json`
记录当前执行状态。构建输入有版本快照，实际回执保留每个坐标使用的版本，
不会把早期有效产物改称由后续快照重建。运行过的脚本、失败包、源树和容器均保留。

候选目录：

```text
~/pgsty/rpm/yum/<platform>/pg-duckdb-1.2.0-20261104/
~/pgsty/deb/apt/<codename>/pg-duckdb-1.2.0-v13-20261104/<arch>/
```

旧 DEB 候选继续保留在原目录，不能作为 v13 的最终交付。DEB 回执分别记录
核心、桥接层的实际编译输入和重新打包使用的 v13 输入。

候选收集、平台验收、生产 staging、签名与公共发布分别记账。
完整矩阵是否完成以最终回执为准，不以配方存在或文件数量判断。

## 下游边界

`pg_mooncake` Rust 包的 `RegisterDuckdbTableAm` C ABI 未变化，未发现需要自动重建的新输入。
但旧 Mooncake C++ 社区插件对应 DuckDB 1.4.3，不能用于 2.0.0；
2026-11-04 检查的两种架构 v2.0.0 公共插件路径均为 404。
本批不声明与现有 Mooncake 插件兼容；等待上游提供匹配插件后另行验收。

2026-11-05：PGSTY fork 的 pg_mooncake 0.3.0 已随包构建匹配的 Mooncake v0.0.2
插件，并在 EL9 / Ubuntu 24.04 ARM64、PG18 上与 pg_duckdb 1.2.0 完成安装和
联合测试。原 0.2.0 社区插件的限制仍成立；新配方与验证记录见 [pg_mooncake](pg_mooncake.md)。

`duckdb_fdw` 使用独立的静态源码输入，不因本次升级自动重建。
同一 PG 主版本的既有互斥关系保留。
