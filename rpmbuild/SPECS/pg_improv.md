# pg_improv 0.13.0 打包

RPM/DEB 使用上游 0.13.0，原生采用 pgrx **0.19.3**，不再应用旧 pgrx
兼容补丁。独立扩展 workspace 位于 `crates/pg_improv`，支持 PG15–18，
Rust 最低版本为 1.97。许可为 Apache-2.0 OR MIT。

- 上游：<https://codeberg.org/gregburd/improv>
- 正式版本：<https://codeberg.org/gregburd/improv/src/tag/v0.13.0>
- 源码：<https://codeberg.org/gregburd/improv/archive/v0.13.0.tar.gz>
- 归档：`improv-0.13.0.tar.gz`
- SHA-256：`1758815bf497d0d9913a1dab465ffc5473272d01674501c414d3d96e675983ef`

```sh
pig build get pg_improv
# 镜像尚无当前归档时，仅复制这一个缺失文件到 builder SOURCES。
pig build pgrx -v 0.19.3 --pg 18
cd ~/rpmbuild
./dep pg_improv 18
./build pg_improv 18
```

配方执行 locked fetch、离线打包和 lockfile 不变检查，保留 release DWARF。
主包安装 SO、control、生成的 0.13.0 安装 SQL 及上游全部迁移脚本，包括
0.12.2→0.13.0。Rust/pgrx 不生成 PGXS bitcode。打包不补写产品功能或迁移。

## 0.13.0 代表性验证：2026-11-07

Rocky Linux 9.8 aarch64 / PG15、16 与 Ubuntu 24.04.5 arm64 / PG15–18
通过构建、主包与调试包 payload、匹配的 ELF/DWARF build-id 和安装检查。
EL9 PG15 与 Ubuntu PG18 另通过上游 `tests/txn.sh`，覆盖事务回滚、
savepoint、commit/logical 模式和 dump/restore。测试从 postgres 可读的
`/tmp` 工作目录运行，未修改上游测试或包内文件。全部平台的后续结果见
`/Users/vonng/pgsty/artifacts/extension-refresh-20261107/`。

## 历史验证：0.12.1，2026-10-28

Rocky Linux 9.8 aarch64 / Ubuntu 24.04.5 arm64、PostgreSQL 18.6 均通过
构建、安装和上游 `txn.sh`、`finance.sh`。主包、RPM debuginfo/debugsource、
DEB dbgsym 的 payload、实际 DWARF 和 build-id 均通过核对；lockfile 未变化。
EL9 只在临时 finance 测试脚本中关闭 logging_collector，避免日志路径冲突。
其他 PG 版本未做本批二进制构建或运行验收。

产物与完整证据：`/Users/vonng/tmp/pgxn-packaging-20261028-hassp03o/`。
本批报告位于本地忽略的 `docs/pgxn-pilot-20261028.md`，未提交或发布。

## 历史验证范围：0.10.0，2026-10-23

以下记录属于旧版，不代表 0.12.1 的其他 PG 版本已通过验收。

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
