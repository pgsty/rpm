# pg_improv 0.10.0 试包

2026-10-23 新增 RPM/DEB 配方。按用户要求，Rust 构建统一为 pgrx **0.19.3**。
上游 0.10.0 的 PG 扩展仍固定在 0.17.0；两侧应用同一份
`pg-improv-0.10.0-pgrx-0.19.3.patch`，更新独立 workspace 的 Cargo.toml/
Cargo.lock，并删除已经废弃的 embed binary 声明和源文件。
不修改产品逻辑或补写 SQL 迁移。

- 上游：<https://codeberg.org/gregburd/improv>
- 正式版本：<https://github.com/gburd/improv/releases/tag/v0.10.0>
- 原始源码：<https://github.com/gburd/improv/archive/refs/tags/v0.10.0.tar.gz>
- 本地归档：`~/pgsty/repo/ext/src/improv-0.10.0.tar.gz`
- SHA-256：`4d27747a90a358750ddd05811687618c1de97e1c73743d97c92d98aed38ad626`
- 补丁 SHA-256：`ec9c111b57fdecfd6021188a20f94a281bac673dc52d96867741df07a924583e`
- License：Apache-2.0 OR MIT；MSRV 1.97；本次 Rust 1.99.0。
- 支持声明 PG15–18；独立 crate 为 `crates/pg_improv`，不是根 workspace。

## 构建

```sh
pig build get pg_improv
# 未发布到源码镜像时，只复制该缺失归档到 builder 的 SOURCES。
pig build pgrx -v 0.19.3 --pg 17
cd ~/rpmbuild
./dep pg_improv 17
./build pg_improv 17
```

配方执行 locked fetch、离线打包、lockfile 不变检查，保留 release DWARF。
主包安装 SO、control、生成的 0.10.0 base SQL 以及上游原有三条 upgrade SQL。
Rust/pgrx 不生成 PGXS bitcode；没有关闭 LLVM 或生成扩展 llvmjit 子包。

## 已验证范围

- `pgsty/el9a:build`：Rocky Linux 9.8 / aarch64 / PostgreSQL 17.11。
- `pgsty/u24a:build`：Ubuntu 24.04.5 noble / arm64 / PostgreSQL 17.11。
- 两侧主包安装、包文件、依赖、非空 DWARF、RPM debugsource 均通过。
  产出 3 RPM、1 DEB、1 dbgsym，已收集到本地 yum/apt 暂存目录。
- 两侧通过上游 `tests/txn.sh` 与 `tests/finance.sh`，覆盖无 preload 使用、
  trigger/commit/logical、事务与 savepoint 回滚、两阶段提交、逻辑槽、
  dump/restore 后继续同步、财务模型与 what-if。
- EL9 财务测试集群临时设置 `logging_collector=off`，避免 RPM 默认日志目录
  与上游脚本的 `log` 文件重名；不改变安装包。
- 精度边界测试确认 `bigint/numeric` 的 `2^53+1` 变为 `2^53`，源表保持精确；
  小数运算也是 f64。what-if 可在只读事务中执行且不改变数据；manual recalc 幂等。
- PG15/16/18 的 pgrx 0.19.3 `cargo check` 通过，但本轮未构建其二进制包或验收运行路径。

逻辑同步要求 preload、`wal_level=logical` 及 `improv.database`；复制槽可能保留 WAL。
包不自动修改数据库配置。该项目仍新，试包通过不代表精确十进制财务引擎或生产成熟度。
本轮未写 PGEXT、提交、推送、进入生产 staging 或发布。

完整证据与精度测试脚本：`/Users/vonng/tmp/new-extensions-20261023/improv/`。
