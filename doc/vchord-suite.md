# Vchord suite 2026-11-04

本批将三套 RPM/DEB 配方统一到 PGSTY 分支，目标为 PostgreSQL 14–18。
三者均由 PGSTY 供应，不因本次升级重建其他下游扩展。

| 扩展 | 版本 | GitHub tag | 源码归档 |
|---|---|---|---|
| vchord | 1.2.0 | `pgsty/vchord`, `1.2.0` | `vchord-1.2.0.tar.gz` |
| vchord_bm25 | 1.0.0 | `pgsty/vchord_bm25`, `1.0.0` | `vchord_bm25-1.0.0.tar.gz` |
| pg_tokenizer | 1.0.0 | `pgsty/pg_tokenizer`, `v1.0.0` | `pg_tokenizer-1.0.0.tar.gz` |

原始 GitHub tag 归档直接保存到 `~/pgsty/repo/ext/src`，没有重新打包。
URL 格式为 `https://github.com/pgsty/<extension>/archive/refs/tags/<tag>.tar.gz`。
SHA256：

```text
caf1a482b62e8eba507c881f3acda3365393fc4d1648ad5ca9d4dd51d47a96a0  vchord-1.2.0.tar.gz
2e2f56b0dc64eafe69508e7dc5d2b3773fab1869875e194a928b3b197f605fb2  vchord_bm25-1.0.0.tar.gz
f59b7ad32fd449709e12fadc67816925daa567bb4014398e82818eca45a7f33d  pg_tokenizer-1.0.0.tar.gz
```

## 构建要点

- 三者使用 cargo-pgrx/pgrx 0.19.3。本批镜像预装 Rust 1.99.0。
- vchord 的 ARM64 SIMD C shim 要求 Clang >= 16 或 GCC >= 14；配方统一显式选择 Clang >= 16，并设置 `CC`、`CXX` 和规范化后的 `LIBCLANG_PATH`。不能把系统旧 GCC 当成可用的默认编译器。
- vchord 使用 RPM 编译标志；EL10 去除不适用于该 Clang 路径的 GCC LTO 标志，保留 `-g`。三个扩展均设置 Rust release debug=2、strip=none。
- vchord 归档中的 workspace 版本 `0.0.0` 是上游设计，扩展版本来自 control。不得改写 Cargo.toml/Cargo.lock 来替换这个占位版本。
- `cargo fetch --locked` 后离线编译，并验证 Cargo.lock 未变化。pg_tokenizer 的 Snowball 依赖固定为 `pgsty/rust-stemmers` tag `v1.2.1`。
- vchord、vchord_bm25 安装分支提供的 release SQL 和全部 upgrade SQL。bm25 自带的 `0.3.0--1.0.0.sql` 会明确拒绝不兼容的原地升级，打包侧忠实保留该行为。
- 三者是 Rust/pgrx 包，没有 PGXS bitcode/index payload，也不生成独立扩展 llvmjit 包；主包不得依赖 LLVM/Clang/core-llvmjit。
- 可用 `--define 'cargo_target_dir /root/cargo-target/vchord'` 指定容器内的 Cargo 缓存位置，在多个 PG 构建间复用依赖；默认仍使用当前源码目录下的 target。

## 代理与验证

宿主机网络请求使用 `http://127.0.0.1:8888`。Mac Docker 容器使用
`http://host.docker.internal:8888`；Linux Docker 容器使用 host 网络并访问
`http://127.0.0.1:8888`。HTTP/HTTPS/Cargo 环境变量及 DNF/APT 代理配置均显式设置。
每个 builder 先执行 `pig build get`，再只补复制当前缺失的三个指定归档，并检查 SHA256。

先导验证已通过：

- `pgsty/el10a:build`：Rocky Linux 10.2、aarch64、PG18，9 个 RPM（主包、debuginfo、debugsource 各 3 个）。
- `pgsty/u26a:build`：Ubuntu 26.04.1、arm64、PG18，6 个 DEB/DDEB（主包、dbgsym 各 3 个）。
- 安装本批主包后，同时 preload 三个库，创建 vector 和三个扩展；验证扩展版本、向量索引、原生 tsvector BM25 排序、tokenizer/BM25 联动查询。
- payload 检查覆盖 control、目标版本 SQL、SO、非空 debug 文件及 RPM debugsource；RPM 运行依赖不含 LLVM/Clang/core-llvmjit。

## RPM 生产矩阵结果

下列六个平台均完成三个扩展的 PG14–18 构建、逐包检查、安装及五个 PG 的联动测试。
每个平台 45 个二进制 RPM，总计 270 个：主包、debuginfo、debugsource 各 90 个。
全部 RPM builder 实际使用 Clang 21.1.8。

| 镜像 | 实际系统 | 架构 | 主机 | RPM 数量 |
|---|---|---|---|---:|
| `pgsty/el8:build` | Rocky 8.10 | x86_64 | m3 | 45 |
| `pgsty/el8a:build` | Rocky 8.10 | aarch64 | m1 | 45 |
| `pgsty/el9:build` | Rocky 9.8 | x86_64 | m3 | 45 |
| `pgsty/el9a:build` | Rocky 9.8 | aarch64 | m5 | 45 |
| `pgsty/el10:build` | Rocky 10.2 | x86_64 | m3 | 45 |
| `pgsty/el10a:build` | Rocky 10.2 | aarch64 | m5 | 45 |

产物已取回 `yum/<el-major>.<arch>/vcs1104/<arch>/`，并逐一核对 SHA256。
日志、镜像 ID、实际环境、源文件及包校验值保存在
`~/.cache/pgext/vchord-suite-20261104/<platform>/`。
RPM/DEB 联合任务使用 m0/m1/m3/m5；m0 的较慢编译任务后续携带缓存迁到 m3 续编。
DEB 十平台结果见兄弟仓库 `deb/docs/vchord-suite.md`。

本批未进入生产 staging，未签名、重建仓库元数据或发布源码/RPM。
`pgext.extension` 中 bm25/tokenizer 的旧版本与源码字段尚未同步；本任务未修改元数据库。

## vchord 1.2.0-2PGSTY 重构建：2026-11-05

按要求重新下载 [pgsty/vchord 的 1.2.0 tag 归档](https://github.com/pgsty/vchord/archive/refs/tags/1.2.0.tar.gz)，
核对 annotated tag `9fe0ac8fd54d80fd7b4f2e8fa4acd9a75f4a3d9c` 指向
`6ea6a3be3b2ec5521f2575055d3c77a0b9771f95`。归档内 288 个文件与该提交逐一匹配。
下载结果与原本地归档完全相同，SHA256 仍为
`caf1a482b62e8eba507c881f3acda3365393fc4d1648ad5ca9d4dd51d47a96a0`。
权威目录中的 `vchord-1.2.0.tar.gz` 已用本次下载刷新；spec 的 Release 从
`1PGSTY` 增为 `2PGSTY`，并记录源码提交、校验值和 changelog。

供应来源保持 PGSTY。本次仅重构建 vchord，范围为六个 RPM 生产平台的 PG14–18。
Cargo.lock 仍为 `8d2e52210bcb7daca5643af4ef8ebe703b86451a8bd6a8fddf3c939464ccbb84`，
每次构建前后均检查未变化。源码文件名、依赖和安装 SQL 没有变化。

| 镜像 | 容器内实际系统 | 架构 | 构建主机 | PG | 二进制 RPM |
|---|---|---|---|---|---:|
| `pgsty/el8:build` | Rocky 8.10 | x86_64 | m0、m4 | 14–18 | 15 |
| `pgsty/el8a:build` | Rocky 8.10 | aarch64 | m1 | 14–18 | 15 |
| `pgsty/el9:build` | Rocky 9.8 | x86_64 | m4 | 14–18 | 15 |
| `pgsty/el9a:build` | Rocky 9.8 | aarch64 | m5 | 14–18 | 15 |
| `pgsty/el10:build` | Rocky 10.2 | x86_64 | m4 | 14–18 | 15 |
| `pgsty/el10a:build` | Rocky 10.2 | aarch64 | m5 | 14–18 | 15 |

EL8 x86_64 的 PG14/15/17 在 m0 构建；PG16/18 在完成其他平台后由 m4 并行补建。
m0 完成 PG15 后停止重复编译，将 m4 产物及日志按 SHA256 核对后汇入，
全部五个 PG 的包在 m0 统一安装验收。各 PG 的构建来源另存 `el8/build-origins.json`。

全部 builder 使用 Rust 1.99.0、cargo-pgrx 0.19.3、Clang/Clang++ 21.1.8，
明确设置 `CC`、`CXX` 和 `LIBCLANG_PATH=/usr/lib64`。
EL10 构建阶段去除 GCC 的 `-flto*`、`-ffat-lto-objects`，保留 `-g`；
Rust release 使用 debug=2、strip=none。保留了原有 Clang 处理，没有使用 `llvm=0` 回退。

每个 builder 先执行 `pig build get vchord`。镜像内的元数据仍指向
`VectorChord-1.1.1.tar.gz`，因此仅补入此次核验的 `vchord-1.2.0.tar.gz`。
依赖下载的镜像连接错误及恢复过程已保留：大部分容器改用腾讯镜像直连，
m1 改用 Rocky/Fedora 官方源经本机代理访问；GitHub 请求始终使用指定的 8888 代理。

验收结果：

- 静态检查、源码解包和六平台 × 五个 PG 的实际构建全部通过。
- 90 个二进制 RPM：主包、debuginfo、debugsource 各 30 个，EVR 均为 `1.2.0-2PGSTY.elN`。
- 逐包确认架构、SO、control 和 17 份 SQL；control、安装及升级 SQL 与上游逐字节一致。
- SO 与 debuginfo 的 Build ID 匹配，debug 包包含 DWARF，debugsource 包包含非空源码。
- 主包没有 LLVM/Clang/core-llvmjit 运行依赖；没有扩展 llvmjit 子包。Rust/pgrx 的本批构建没有 PGXS bitcode/index payload。
- 全部 30 个独立数据库环境通过 preload、CREATE EXTENSION、版本检查、vchordrq/vchordg 索引查询及计划检查、halfvec 查询、事务回滚、UPDATE/DELETE、VACUUM、REINDEX、pg_dump/pg_restore 验证。
- 90 个 RPM 共 650,940,164 字节，已取回 `yum/<el-major>.<arch>/vcr1105/<arch>/`，逐一核对 SHA256；每个平台目录附有 `SHA256SUMS`。

完整证据位于 `~/.cache/pgext/vchord-reissue-20261105/`：`receipt.json`、
`packages.json`、`SHA256SUMS`、源码 provenance、镜像 ID、环境、构建和测试日志，
以及 SRPM 归档。临时 builder 已停止，容器及其构建缓存保留。

这次归档与前次源码相同，未包含对[此前记录的 vchordg/halfvec 排序问题](vchord-suite-qa-20261104.md)的修复。
本批已完成静态检查、代表性验证、六平台生产矩阵及本地取回验收。
尚未进入生产 staging，未签名或重建 YUM 元数据，未同步源码镜像或发布 YUM；
未修改 DEB 配方或 pgext 元数据。

## 2026-11-05 本地入库与目录同步

后续入库验收已将本批 30 个主 RPM 加入六个平台的正式 YUM 索引，
60 个 debug RPM 独立归档；DEB 同修订的 50 个主包也已入库。
签名、索引与客户端下载验收通过，回执见
`~/pgsty/repo/reports/daily-package-final-20261105.md`。
本地 PGEXT 目录与双语 changelog 已记录 `1.2.0-2PGSTY` 重构建，
扩展版本字段仍为 `1.2.0`。CDN 与源码镜像尚未同步。
