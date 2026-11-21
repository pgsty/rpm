# pg_duckdb 1.2.1 升级与 PG19 核验

本轮将 pg_duckdb 1.2.0 升至上游正式发布的 **1.2.1**（2026-11-20），
使用该版本实际 gitlink 固定的 **DuckDB 2.0.1**。目标为 PG15–19；PG14、EL8 已移出当前配方目标。
证据只覆盖下表列出的两个代表性平台，未展开四平台生产矩阵。

## 固定输入

| 输入 | 版本或 commit |
| --- | --- |
| pg_duckdb | `451d389a3fe9d179b06172c6a3595d291de7ca76`（v1.2.1） |
| DuckDB gitlink | `8d78114e90a53823803660bf821f6073ac87da8c`（v2.0.1） |
| httpfs CMake 固定输入 | `f71cfdb4bff85b9e15b1f3b842d9aa395aff0167` |
| 私有 curl（仅系统 curl <7.85 时） | 8.23.0；u24 使用系统 libcurl 8.5.0 |

权威归档：`~/pgsty/repo/ext/src/pg_duckdb-1.2.1.tar.gz`，根目录 `pg_duckdb-1.2.1/`。
SHA256：`9d4d6b6eb8100ced1ff82a9e2f641dc3440d2547dd6de2aedeccfdee1af7e3aa`。
它包含固定 DuckDB 源码与 `SOURCE_MANIFEST.json`，不包含 httpfs checkout；
httpfs 仍通过上游 CMake 的固定提交获取，两侧实际 checkout 均已核对。
归档使用 GNU tar 和 `COPYFILE_DISABLE=1`，排除 Git 与 AppleDouble 元数据。

curl 归档 SHA256：`e3de77cfa6367083c776a26647fc9f633b538c06c3baa73d931a252ac8f72b49`。
每次构建先执行 `pig build get pg_duckdb`；本批新归档在公共镜像返回 404 后才按具体文件复制。
未发布源码镜像或二进制包。

## PG 版本证据

| PG | EL9.8 / aarch64（m1） | Ubuntu 24.04.5 / amd64（m3） |
| --- | --- | --- |
| 15 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 |
| 16 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 |
| 17 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 |
| 18 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 |
| 19 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 | 构建＋包/debug＋运行＋core LLVM/JIT 通过 |

表内通过必须同时满足：主包成功生成、LLVM bitcode/index 属于主包、
运行依赖无 LLVM/Clang/core llvmjit、debug 包非空且 ELF Build-ID 匹配、
核心与桥接层都有类型/变量 DWARF、隔离实例实际预加载与查询通过、
全部 bitcode/index 可由 core 对应 LLVM 读取且实际 JIT/inlining 查询成功。
上游源码 gate 已包含 PG19；最终支持判定以逐版本 receipt 为准。
PG18/19 模块版本必须报告 `v1.2.1`，SQL 扩展版本为 `1.2.1`，DuckDB 运行版本为 `v2.0.1`。

## 补丁审查

| 当前补丁 | 必要性 | 最小范围与充分性边界 |
| --- | --- | --- |
| `pg_duckdb-1.2.1-source-archive.patch` | 官方 GitHub tar 无子模块 Git 元数据；并行安装需先创建 PGXS lib 目录 | 仅 Makefile 三个 hunk；使用随包 DuckDB CMakeLists 作为依赖、去掉 git submodule update、增加 order-only 安装依赖；不改运行时代码或依赖 pin |
| `pg_duckdb-1.2.1-private-curl.patch` | EL9 系统 curl 缺少 httpfs 要求的 >=7.85 API | 单独 28 行 helper，仅在旧系统 curl 上构建私有 PIC 静态库；发行版 DWARF/hardening flags 传入，不替换系统库 |

补丁统一使用 `extension-version-purpose.patch` 命名，两仓库逐字一致。
旧 httpfs `unique_ptr` 返回值修复已在新固定提交中直接使用 `std::move(result)`，删除本地重复修复。
EL8 专属 flags/GCC Toolset/OpenSSL3 分支随目标退役删除；未引用的旧 install-order patch 删除，
其必要顺序约束保留于新的 source-archive patch。
当前没有新增 PG19 API 或执行器兼容补丁。

## 构建、缓存与调试信息

m1：`pgsty/el9a:build`，容器 `nrheavy-pg-duckdb-el9a`，上限 6 CPU / 24 GiB，核心编译并行 2。
m3：`pgsty/u24:build`，容器 `nrheavy-pg-duckdb-u24`，上限 12 CPU / 40 GiB，核心编译并行 4。

RPM PG16–19 使用 builder 默认 `w19.zstdio`。按用户授权，仅在尚未启动的 PG15 验证构建追加
`--define '_binary_payload w3.zstdio'`，降低封装压缩耗时；不改 spec、源码、编译 flags 或核心缓存。
PG16 在切换检查时已经启动，因此保持原参数；全部坐标仍执行同样的包/debug/runtime/JIT 验收。

EL9 builder 初始缺 pgdg19 仓库导致 `No match for argument: postgresql19-server`；
在本批独立容器中补充与既有 PGDG mirror 一致的 pgdg19 配置后安装 PG19.0。
EL9 PGXS 的 `LLVM_BINPATH` 指向 LLVM21，而系统默认 clang 已为 22。
配方传入 `CLANG='$(LLVM_BINPATH)/clang'`，保留 PGXS 指定的 llvm-lto，
并声明 EL9 平行 `clang21 llvm21` 构建依赖，使 bitcode 生产者与 PGDG core 一致。
u24 使用 PGXS LLVM19；每个 PG 均检查 core 与 reader 链接同一 libLLVM，
逐个读取包内 bitcode/index，并运行强制开启 JIT/inlining 的 PG 聚合和扩展 C 函数调用。
本批 PG19 新建实例默认 `jit=off`；验收显式 `SET jit=on` 后通过。
该开关调整只在测试会话中生效，原始探测失败与修正后 receipt 均保留。

核心、桥接层和私有 curl 均保留完整发行版 `-g`，移除旧核心 `-g1` 限制。
跨 PG 复用只限同平台同源码、补丁、编译器、依赖及 flags 的 bundled DuckDB 缓存；
桥接对象和 LLVM bitcode 仍逐 PG 编译。
DEB 首轮在完整核心 DWARF 上触发 `dwz: Too many DIEs, not optimizing`；
仅 `libduckdb.so` 排除 DWZ 压缩，桥接层仍使用逐 ELF DWZ，`dh_strip` 正常分离完整 dbgsym。
staged 核心使用确定性 PG 专属 Build-ID，避免共装路径冲突。
RPM 保留 ELF Build-ID，但不生成跨 PG 冲突的全局 Build-ID 符号链接。

## 准确复现命令

在任务专属容器内运行，先确认两份指定源码及本轮 spec/recipe/patch 已就位。
以下示例为 PG19；将版本依次替换为 18、17、16、15 可重建其余坐标。
准确复现本批 RPM PG15 时，还需追加 `--define '_binary_payload w3.zstdio'`；其它坐标使用默认压缩。

```bash
# m1 / nrheavy-pg-duckdb-el9a
# BuildRequires include parallel clang21/llvm21 for PGDG EL9 PGXS.
pig build get pg_duckdb
rpmbuild -ba /root/rpmbuild/SPECS/pg_duckdb.spec \
  --define 'pgmajorversion 19' --define 'duckdb_core_jobs 2' \
  --define '_topdir /root/rpmbuild' \
  --define '_rpmdir /root/nonrust-heavy-20261121/pg_duckdb/artifacts/el9a/rpm' \
  --define '_srcrpmdir /root/nonrust-heavy-20261121/pg_duckdb/artifacts/el9a/srpm'

# m3 / nrheavy-pg-duckdb-u24
pig build get pg_duckdb
cd /root/nonrust-heavy-20261121/pg_duckdb/debbuild/pg_duckdb
make build19 DUCKDB_MAX_JOBS=4 \
  PKG_OUTPUT_DIR=/root/nonrust-heavy-20261121/pg_duckdb/artifacts/u24
```

DEB 的专属 Makefile 按当前 PG 目标直接从 `control.in` 生成 control，
未使用 `pg_buildext updatecontrol`。因此旧镜像中 helper 的默认 PGDG 列表止于 18
不会漏掉本批 PG19；PG19 主包、dbgsym 和安装运行记录均实际存在。
无需为该镜像问题改动 pg_duckdb recipe 或全局 helper。

## 验收与外部证据

日志、输入 SHA、每轮首错、产物清单、复现脚本及结果保存在：
`~/pgsty/artifacts/nonrust-heavy-20261121/pg_duckdb/`。
入口为 `result.json`；每个坐标各有 build 与 verify receipt，原始失败记录不覆盖。

核心 smoke 覆盖 `CREATE EXTENSION`、真实 DuckDB 执行计划、PG 表扫描/聚合、事务回滚、
DuckDB 临时表、JSON、Parquet 导出/导入、httpfs 本机 HTTP 读取，
以及上游提供的 `1.2.0 → 1.2.1` SQL 升级路径。
HTTP 测试只在隔离实例允许加载本批构建的 unsigned httpfs 插件；不代表公共签名插件、
MotherDuck 或外部云认证集成已通过。

本记录对应两个代表性平台，未执行四平台生产构建或发布。
PGEXT 与全量矩阵按最终 verified 坐标更新 `extension` / `universe` 的
`version`、`rpm_ver`、`deb_ver` 与 PG 范围。
`pg_mooncake` Rust 配方冻结，未推断其社区插件与 DuckDB 2.0.1 兼容。
`duckdb_fdw` 的独立静态输入不自动沿用本批结论。

<details>
<summary>历史：1.2.0 批次记录（不作为本轮 1.2.1 验证证据）</summary>

## pg_duckdb 1.2.0 候选构建

本轮打包 pg_duckdb 1.2.0 与其固定的 DuckDB 2.0.0，目标是
EL8/9/10 × x86_64/aarch64，以及 Debian 12/13、Ubuntu 22.04/24.04/26.04
× amd64/arm64，全部覆盖 PG14–18。共 80 个坐标，预期 90 个 RPM
（主包、debuginfo、debugsource）和 100 个 DEB（主包、dbgsym）。
SRPM、buildinfo、changes 和验收证据另行保存，不计入这 190 个二进制包。

上游将 [v1.2.0](https://github.com/duckdb/pg_duckdb/releases/tag/v1.2.0)
标为 Experimental。构建和隔离验收不改变这一定位。
本轮只收集候选，不进入生产 staging，不签名、发布或写入 PGEXT。

### 源码与依赖

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

### 打包修复

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

### 构建与验收方法

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

### 证据与交付位置

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

### 下游边界

`pg_mooncake` Rust 包的 `RegisterDuckdbTableAm` C ABI 未变化，未发现需要自动重建的新输入。
但旧 Mooncake C++ 社区插件对应 DuckDB 1.4.3，不能用于 2.0.0；
2026-11-04 检查的两种架构 v2.0.0 公共插件路径均为 404。
本批不声明与现有 Mooncake 插件兼容；等待上游提供匹配插件后另行验收。

2026-11-05：PGSTY fork 的 pg_mooncake 0.3.0 已随包构建匹配的 Mooncake v0.0.2
插件，并在 EL9 / Ubuntu 24.04 ARM64、PG18 上与 pg_duckdb 1.2.0 完成安装和
联合测试。原 0.2.0 社区插件的限制仍成立；新配方与验证记录见 [pg_mooncake](pg_mooncake.md)。

`duckdb_fdw` 使用独立的静态源码输入，不因本次升级自动重建。
同一 PG 主版本的既有互斥关系保留。

</details>
