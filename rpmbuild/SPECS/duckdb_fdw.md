# duckdb_fdw 独立静态打包

当前设计：duckdb_fdw **2.0.2** 内嵌从源码构建的 DuckDB **2.0.0**，同一 PostgreSQL 主版本与 `pg_duckdb` 安装互斥。此文件记录 2026-10-24 的代表性验收及后续完整矩阵验收，不是发布记录。

独立包相关文件：`rpmbuild/SPECS/duckdb_fdw.spec`、本目录的记录文件、`rpmbuild/Makefile` 的 duckdb_fdw 目标及平台说明、新 `patches/duckdb_fdw-2.0.2-static.patch`，以及 `bin/duckdb-fdw-smoke.sql` / `bin/duckdb-fdw-httpfs.sql`。旧 `patches/duckdb_fdw-2.0.1.patch` 删除。

## 2026-10-24 全矩阵补充验收

在首轮代表性验收之后，又以本轮新构建的二进制包完成 **16 个平台 × PG15–18，共 64 个主包坐标**。六个 RPM 平台为 EL8/9/10 × x86_64/aarch64；十个 DEB 平台为 bookworm/trixie/jammy/noble/resolute × amd64/arm64。

| 范围 | 构建、包/ELF/DWARF、SQL/Parquet、11 个 examples、取回 | PG18 官方 httpfs、LLVM JIT、双向安装冲突、残留 preload/重启 |
|---|---|---|
| EL8、EL9、EL10，双架构 | 24/24 通过 | 6/6 平台通过 |
| bookworm、trixie、jammy、noble、resolute，双架构 | 40/40 通过 | 10/10 平台通过 |

每个 PG 都执行原样上游 installcheck，仍保留已知 EXPLAIN CAST 与空行/对齐预期差异；仅规范化这些差异后 SQL 输出一致，不能宣称原样回归全绿。插件/JIT/残留 preload 检查限于每个平台 PG18。全部上游 control 与 11 个 SQL 文件原样安装并逐文件比较。

EL8 完整构建发现 GCC8 在 DuckDB `filter_combiner.cpp:1174` 的 reference_wrapper 转换错误。RPM spec 仅在 EL8 改用 GCC Toolset 15、匹配 annobin 和 C17 native C 语义后，双架构 PG15–18 全部通过。EL10 直接 rpmbuild 编排恢复仓库 wrapper 已有的 `QA_RPATHS=3`，并验证实际 RUNPATH 仅为对应 PG 库目录。Ubuntu 26.04 的符号比较脚本固定 `LC_ALL=C` 解决 uutils sort/comm 的 locale 排序差异，原包重验通过；未修改 DEB recipe 或通用源码补丁。EL8 HTTP 测试兼容 Python3.6。原失败日志均保留。

本轮产物已取回本地 `rpm/yum/<el>.<arch>/` 与 `deb/apt/<codename>/`：24 RPM 主包、24 debuginfo、24 debugsource、24 SRPM；40 DEB 主包、40 dbgsym、10 buildinfo、10 changes，共 **196 个文件**。所有文件独立复核 SHA-256 和大小，DEB 元数据引用与实际文件一致；全部路径被 Git 忽略。

完整矩阵、实际系统/工具链、逐文件哈希、失败与重试记录位于 `/Users/vonng/tmp/duckdb-fdw-matrix-20261024/REPORT.md`、`verification.json`、`artifacts/manifest.json`、`environments/` 和 `logs/`；复现入口为该目录的 `REPRODUCE.md`。未复用首轮代表性二进制包。完整 DWARF、LLVM bitcode/index、动态插件均保留，未用 llvm=0 回退。

必要修复与本文记录保持未提交。未导入生产 staging、签名、发布源码/YUM/APT 或写入 pgext；未重编 pg_duckdb。下面的首轮记录保留其当时的验证范围和制品哈希，后续支持范围以上述矩阵为准。

## 来源与旧补丁审查

| 项目 | 正式 tag | commit | 源码归档 SHA-256 |
|---|---|---|---|
| [duckdb_fdw](https://github.com/alitrack/duckdb_fdw/releases/tag/v2.0.2) | v2.0.2 | `4c444d19f80eace50bc09fa3ec766e8ca2cf667d` | `1ed7935b009211915434fd65083b0562389e3faf1722865f81633d70a0c0fc8b` |
| [DuckDB](https://github.com/duckdb/duckdb/releases/tag/v2.0.0) | v2.0.0 | `d54cbbe3df17e8e5ce68312f483b4155836112aa` | `7e89053255046bfb26afbd7f524a2fb84df7dbef496aa911ea35e4a1182fdc00` |

两者均为非 draft、非 prerelease 正式 release。FDW tag 是 annotated tag，tag 对象为 `ee274ae7b17b0df6dad33de95feadf83ae837bb0`。校验值是下载官方 tag 归档后本地计算并固定的值，不是上游单独签署的校验声明。

最终源码位于 `/Users/vonng/pgsty/repo/ext/src/duckdb_fdw-2.0.2.tar.gz` 和 `duckdb-2.0.0.tar.gz`。不修改、冒用旧的 `2.0.1+git20260529.9354241` 归档。

原 `duckdb_fdw-2.0.1.patch` 已撤销，逐项处理如下：

- planner API、PG18 explain 头文件、slot 初始化：正式上游已有对应实现，撤销旧修改；PG14 的 Boolean 节点 API 缺口另见推广评估。
- 缺省 user mapping、连接初始化、事务清理、类型转换：正式上游已重写相关路径，采用上游实现。
- UPDATE/DELETE 回归预期、普通文本方括号处理：采用正式上游测试和修复。
- 旧 SQL 升级语法补丁：不继承；忠实安装上游所有 control/SQL/升级脚本。
- 从 pg_duckdb 取头文件、软链接 `libduckdb.so`、RPATH、旧 ABI 开关、共享 runtime 共存补丁：移除。
- 新补丁只处理独立静态构建、静态扩展注册、运行时来源检测及互斥策略。

## 链接与运行边界

构建使用发行版编译、加固、调试 flags 和 PIC。显式链接 DuckDB core、HTTP/动态加载能力以及 core_functions、Parquet、JSON、ICU 静态归档，不依赖 `-lduckdb` 搜索，不安装通用 `libduckdb.so`。系统 libc/libstdc++ 等仍动态链接。FDW 的 PGXS bitcode 和 index 进入主包，调试符号由 RPM/DEB 自动拆分。

EL9 GCC 11.5 的 LTO 链接产物在文件库 `INSERT` 上触发 `PhysicalBatchInsert::GetDataInternal` 的 NULL state 内部错误；内存库路径正常。官方 2.0.0 CLI 和同一批 PIC fat archives 以 `-fno-lto` 链接的独立 C API、PostgreSQL 原型均通过同一插入测试。因此最终 native 链接显式使用 `-fno-lto`，保留发行版的编译优化、加固和 DWARF。这与 PGXS 的 Clang bitcode/LLVM JIT 是不同路径，后者继续启用。未修改 DuckDB 执行器源码或绕过该 SQL 测试。

本方案保留 DuckDB 公共符号并使用 `-Bsymbolic` 约束自身定义的内部绑定。初次 ELF 检查发现，仅此参数仍留下 GNU unique 数据符号与动态重定位；最终 core 使用 `-fno-gnu-unique`，重新从源码完整构建。最终 EL9 ELF 的 GNU unique 定义为零，对自身导出定义的 `JUMP_SLOT/GLOB_DAT` 重定位交集为零。保留必要的 C API、C++ 和第三方导出，官方动态 httpfs 实测可用。

这些措施不隔离 PostgreSQL 的全局 ELF 加载命名空间，尤其不能保证之后加载的另一 DuckDB 核心不会误绑定。EL9 最终模块有 55,914 个导出定义，其中 25,200 个也存在于 pg_duckdb 1.1.1 的 DuckDB 核心。`_PG_init` 和查询时检查都晚于 `dlopen` 的重定位与构造函数，不能当作完整共存保护。要在不修改 pg_duckdb 源码的前提下保证反向加载也明确拒绝，需要额外的加载控制或完整隔离；本次不引入这些机制。因此采用同 PG 主版本的软件包安装互斥，不添加 Replaces、不覆盖其文件。

FDW 的 `Conflicts: pg_duckdb_%{pgmajorversion}` 已能阻止两种安装顺序。`pg_duckdb.spec` 同步维护反向 `Conflicts: duckdb_fdw_%{pgmajorversion}`，仅修改配方，未重编 pg_duckdb；反向声明随其下次打包生效，当前 FDW 的保护不依赖该重编。两侧声明均只限制对应 PG 主版本。

插件结论限于实际证据：官方 v2.0.0 ARM64 httpfs 使用 `httpfs_duckdb_cpp_init`，携带自己的部分 C++ 实现，没有强未解析的 `duckdb::` 符号（`logs/httpfs-symbols.log`）。不能仅凭此插件通过就宣称完全隐藏核心后所有动态 C++ 插件仍兼容；本次未验收完全隐藏核心的版本，也没有静默取消动态插件功能。

运行时 guard 以 `dladdr` 返回的 ELF 基址核对嵌入核心所属模块，并扫描已加载的 pg_duckdb 和外部 libduckdb。不根据 control 文件是否存在拒绝，也不伪造库文件名。保留清晰错误和重启提示；禁止原有 unsupported override 绕过此包的互斥策略。

从 pg_duckdb 模式切换到 FDW 模式时，修改 `shared_preload_libraries` 并重启 PostgreSQL。卸载/替换包不会卸载已有服务器进程内的库；新连接仍可能继承 postmaster 预加载的旧库。不同数据库或查询顺序不构成隔离。不能承诺同一 backend 内临时切换。

## 首轮代表性验证与复现

工作证据目录：`/Users/vonng/tmp/duckdb-fdw-20261024/`，包含官方 release/tag JSON、下载校验、原工作树状态、构建与测试日志以及最终产物。

已按顺序完成 `pgsty/el9a:build` / PG18 和随后 `pgsty/u24a:build` / PG18 的代表性完整包与运行验收。首轮尚未执行生产矩阵；后续完整矩阵见上文。两轮均未导入仓库、签名、推送或发布；pgext 元数据更新仍为外部待办。

### EL9 aarch64 / PG18

实际环境：Rocky Linux 9.8，aarch64，PostgreSQL 18.6，GCC 11.5.0，CMake 3.31.8，Clang/LLVM 21.1.8。镜像为 `pgsty/el9a:build`（本地 ID 前缀 `4ded3132fa57`），隔离容器为 `duckdb-fdw-20261024-el9a` 和 `duckdb-fdw-20261024-el9a-peer`。

| 验收项 | 结果与证据 |
|---|---|
| 完整 RPM/SRPM | 干净 `%prep` 起始的 `rpmbuild -ba` 退出 0，`logs/el9a-release-build.log` |
| 主包、debuginfo、debugsource | 三个包均非空，真实 DWARF 和源码，`logs/el9a-package.log` |
| 文件和依赖 | 无通用 libduckdb.so，无 pg_duckdb/libduckdb/LLVM/Clang 直接运行依赖；主包包含 `.bc` 与 thin index；包私有文档/许可证路径 |
| ELF | 无 libduckdb DT_NEEDED、无强未解析 DuckDB 核心依赖，RELRO/NOW、PG magic/init/SQL 导出完整；`logs/el9a-elf.log` |
| 独立运行 | CREATE EXTENSION=2.0.2，引擎 v2.0.0；读写、回滚、NULL、decimal、timestamptz、数组、方括号文本通过 |
| Parquet/httpfs | 内建 Parquet 与官方 v2.0.0 httpfs 的回环 HTTP Parquet 读取通过；保存同 backend 的实际模块映射 |
| LLVM | 主包 bitcode/index 完整；另在验收容器安装 PostgreSQL 自身的 JIT provider 后，实际 JIT 的 4 个函数、inlining/optimization 和 FDW SQL 函数调用通过 |
| 上游测试 | 11 个适用 SQL examples 通过；原样 installcheck 的预期文件差异见下节 |
| 包互斥 | 两种安装顺序均由 RPM 拒绝，原包保持安装；`logs/el9a-fdw-first-conflict.log`、`logs/el9a-peer-tests-final.log` |
| pg_duckdb 单独运行 | 原有 1.1.1 包，实际核心 v1.4.3，duckdb.query 与强制执行 sum=55 通过，未重编 |
| 旧库残留 | 保持 pg_duckdb 预加载进程，正常卸包/装 FDW 后，两个全新 backend 的 CREATE 与 LOAD 均明确拒绝，postmaster 存活；修改预加载并重启后 FDW 正常 |

最终日志使用 `el9a-release-build.log`、`el9a-package.log`、`el9a-elf.log`、`el9a-runtime.log`、`el9a-qa-final/`、`el9a-peer-qa-final/`。带 `initial`、`before-unique`、`native-probe` 的文件和 `m5-el9a-build.log` 是调查原型，不能当作最终验收结果。

### Ubuntu noble arm64 / PG18

EL9 完成后，使用相同源码和逐字一致补丁在 Ubuntu 24.04.5 LTS / arm64 完成主 DEB 与自动 dbgsym 构建和同一组运行验收。实际 PG 为 18.6-1.pgdg24.04+2、GCC 13.3.0、CMake 3.28.3、Clang/LLVM 19.1.1。ELF、独立 SQL、Parquet/httpfs、实际 JIT、两个包安装顺序、pg_duckdb 单独运行、残留 preload 拒绝及重启恢复均通过；原样上游回归的预期差异与 EL9 相同。

DEB 平台局部适配：`dwz` 因静态核心的 DIE 数量过多而失败，仅对该 `.so` 跳过 DWARF 去重，由 `dh_strip` 正常拆出完整 dbgsym。最终依赖为对应 PG 主包和系统 libc/libgcc/libstdc++。完整记录在 DEB 仓库 `debbuild/duckdb_fdw/README.md`；最终日志为 `logs/u24a-final-package.log`，运行证据为 `u24a-qa-final/` 和 `u24a-peer-qa-final/`。noble 的完整二进制打包以 `-nc` 复用首次从源码构建的 core 归档，重新运行 FDW native/LLVM、install 和所有打包步骤，未用手工 `.so` 代替 DEB。

### 最终产物

产物位于证据目录的 `artifacts/el9a/` 和 `artifacts/u24a/`，没有导入 YUM/APT staging。`artifacts/manifest.json` 包含每个文件的完整 SHA-256 和字节数。

| 产物 | 大小（字节） | SHA-256 |
|---|---:|---|
| RPM 主包 | 19,056,883 | `98351588d2ba9bd4bed23eef7436d3c9534a2d1736508a96c5c28526e4b9bcb8` |
| RPM debuginfo | 880,956,836 | `6cd091f788834e49a1aea4ad136aa30050cac435d8252c1928ff538f8447d588` |
| RPM debugsource | 8,376,444 | `336e183196646d86542b4accb045f8604a4fcddefaf57aafd63fbe3e53401107` |
| DEB 主包 | 19,723,466 | `4c6aa7550c29bdd7465dd9718aafd87bf9780c689ba46edb6cf3d936a3906d2b` |
| DEB dbgsym | 912,137,500 | `c7dd5918d3badd842836d37d7c4d327b2c13fc03c4ebf13a73d5ca67b8234c8e` |

另保存了 SRPM、DEB buildinfo/changes；没有生成 DEB source package。大体积调试包来自完整 DuckDB 核心 DWARF，后续应按每个 PG/平台预留制品空间，不以删减调试信息规避。

### 上游回归状态和覆盖边界

未改写上游 SQL、control、升级脚本或 expected 文件。原样 `make installcheck` 已执行，但报告失败：上游 expected 中的 EXPLAIN 少了实际的 `CAST("s" AS VARCHAR)`，并有四处空行差异。保留完整 `regression.diffs`；仅规范化该处 EXPLAIN 和输出格式后，所有 SQL 结果一致。不能将此描述成“原样上游回归全绿”。11 个 examples 不含需要另装 pgvector 的可选示例。

安装互斥是受支持边界。已经验证 pg_duckdb 预加载在先、替换包后 FDW CREATE/LOAD 在后的残留库场景；这时即使目标数据库没有 CREATE EXTENSION pg_duckdb，也必须拒绝。未承诺手工复制库、绕开包管理器、FDW 在先再加载其他核心等任意顺序安全。control 文件存在本身不构成已启用；另有 `logs/el9a-control-presence.log` 验证。

RPM 基本流程（仅隔离容器）：

```sh
cd /root/rpmbuild
pig build get duckdb_fdw
pig build get duckdb_fdw-2.0.2.tar.gz duckdb-2.0.0.tar.gz
# 镜像尚未提供新源码时，只复制上面的两个确定缺失归档。
./dep duckdb_fdw 18
cp SPECS/patches/duckdb_fdw-2.0.2-static.patch SOURCES/
rpmbuild -ba --define 'pgmajorversion 18' --define 'duckdb_core_jobs 12' \
  --define '_smp_mflags -j12' --define '_binary_payload w7.zstdio' \
  SPECS/duckdb_fdw.spec
```

最终构建完整执行 prep/build/install/debug 拆分和 RPM/SRPM 打包，没有使用 `--noprep` 或 `--short-circuit`。`w7.zstdio` 只降低验收制品的压缩等级，保留完整 payload 和调试信息；配方不改变仓库默认压缩设置。

`bin/duckdb-fdw-smoke.sql` 验证实际引擎、读写/回滚、NULL、decimal、timestamptz、数组和普通文本、Parquet。`bin/duckdb-fdw-httpfs.sql` 使用匹配 v2.0.0 的官方 `httpfs`，验证加载及回环 HTTP Parquet 读取。仅在一次性数据库执行。

官方测试插件来自 `https://extensions.duckdb.org/v2.0.0/linux_arm64/httpfs.duckdb_extension.gz`，压缩文件 SHA-256 为 `f524888fc7d74cc0c6c4a8f7ed5beedac5b12e71cb426503f882c72ce6afbd43`。它是测试输入，不打入 FDW 包。

完整安装、运行、双向包冲突和残留预加载测试命令见证据目录的 `REPRODUCE.md` 和 `work/`；所建 PostgreSQL 集群仅在独立容器内，使用 `/tmp` 目录、Unix socket 和 55432/55433 端口，未操作用户数据库。

## 首轮范围与后续验证

首轮完整验证坐标只有两个 ARM64 PG18；后续 64 坐标矩阵已补齐 PG15–18。另在 EL9 对 PG14.24 做了单独 native/LLVM 编译探测（没有安装包或运行数据库）：正式 2.0.2 的 `duckdb_fdw.c:1747` 使用 PG14 没有的 `boolVal`，`:2357` 使用 `makeBoolean`，LLVM 编译明确失败。日志为 `logs/el9a-pg14-compile-probe-final.log`。没有为此关闭 LLVM；PG14 适配列为后续任务，默认 RPM/DEB 入口、spec 版本门槛和 debian/pgversions 收敛到 PG15–18。这次范围调整不改变 PG18 的编译、链接、依赖和 payload。

后续矩阵已按 PG17 优先的顺序补齐 PG15–18，以及各目标系统的原生 x86_64/ARM64 包与 PG18 官方插件验收。PG14 仍需由上游或单独兼容补丁解决节点 API 后再验收，不在本轮支持范围。

首轮 EL8 仅做了有限尝试（后续完整构建发现错误并完成工具链适配，见上文）：`pgsty/el8a:build`，镜像 ID 前缀 `8ba85800f972`，Rocky 8.10 / aarch64 / PG18.6 / 默认 GCC 8.5.0 / CMake 3.26.5 / Python 3.6.8；依赖安装后 LLVM/Clang 为 21.1.8。先 `pig build get`，仅在两个固定归档 404 后复制缺失文件；`./dep duckdb_fdw 18` 成功。以 2 jobs 执行 `timeout 180s rpmbuild -bc --define 'pgmajorversion 18' --define 'duckdb_core_jobs 2' --define '_smp_mflags -j2' SPECS/duckdb_fdw.spec`，配置通过并完成 88/2,018 个步骤后达到时限（退出 124）。未观察到真实编译错误，末尾 `interrupted by user` 来自 timeout，不能当作编译器不兼容证据。没有完成 ELF、RPM、LLVM bridge 或运行验收，也没有切换工具链、禁用 LLVM或开展移植；当时 EL8 状态为待验证。日志为 `logs/el8a-environment-get.log`、`el8a-dependencies.log`、`el8a-probe.log`。

PG14 范围收敛后，已比较 PG18 的展开 spec，除注释外相同（`logs/rpm-final-scope-check.log`）；仅刷新 SRPM 以包含最终 spec，PG18 二进制包保持上述已验收文件。官方 2.0.2 的 `.github/workflows/build_and_test.yml` / `release.yml` 也只列 PG15–18，但上游 CI 配置不能替代本配方的实际验收。

pg_duckdb 及其消费者没有使用本次新构建输入，无须因本包独立静态链接而重编。只对实际有编译、链接或 ABI 变化的消费者另行安排。

## 外部待办

未修改 pgext 元数据库。后续在授权元数据更新时，需要将 upstream/RPM/DEB 版本设为实际验证值，source 改为两个新归档，移除 pg_duckdb 运行依赖，记录同 PG 主版本安装互斥。元数据应使用本轮实际完成的 PG15–18 矩阵范围，不能扩大到 PG14 或未经检查的其他平台。
