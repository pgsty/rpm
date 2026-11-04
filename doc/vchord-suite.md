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
