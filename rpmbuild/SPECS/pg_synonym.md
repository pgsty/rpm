# pg_synonym

官方 [v1.0.0](https://github.com/Mazuco/pg_synonym/releases/tag/v1.0.0) 的 C/PGXS 配方，
PostgreSQL License，PG15–18。包版本为 `1.0.0`，control/SQL 版本为 `1.0`，未修改上游代码。

原始归档 `pg_synonym-1.0.0.tar.gz` 来自
<https://github.com/Mazuco/pg_synonym/archive/refs/tags/v1.0.0.tar.gz>，
SHA-256 为 `8d410728828d8b0d8dca1c40d525b3fbdd3f1c31f5a287c1dc415a53973f815e`。
权威归档位于 `~/pgsty/repo/ext/src/`。

在 EL builder 中先取源；失败后仅补充这一归档，不填充 macOS 仓库的 `rpmbuild/SOURCES`：

```bash
cd ~/rpmbuild
pig build get pg_synonym
./dep pg_synonym 15 16 17 18
./build pg_synonym 15 16 17 18
```

2026-10-23 的代表性验证覆盖 `pgsty/el9a:build`（Rocky Linux 9.8 / aarch64）与
`pgsty/u24a:build`（Ubuntu 24.04.5 noble / arm64）的 PG15、16、17、18。
RPM 共 12 个二进制包，包括非空 debuginfo 和 debugsource；DEB 共 4 个主包和 4 个 dbgsym。
主包含真实 LLVM bitcode/index，无扩展 llvmjit 子包及 LLVM/Clang 运行依赖。

各目标 PG 的上游 5 项 regression 全通过，覆盖 DDL/DML、late binding、权限和 RLS。
两侧 PG17 另验证 DDL 事务回滚、`pg_dump -Fc` / `pg_restore --exit-on-error`，以及恢复后
别名查询和新增列继续同步。扩展使用 event trigger，必须由超级用户安装，不需要 preload。
别名是 security-invoker view；手工修改别名视图或 schema 不在支持路径内，视图重建可能
重置手工添加的 GRANT。

已安装包的 builder 中可从源码目录复现回归：

```bash
PGHOST=/tmp PGPORT=5417 PGUSER=postgres make PG_CONFIG=/usr/pgsql-17/bin/pg_config installcheck
```

临时构建、payload、运行测试与产物清单位于
`/Users/vonng/tmp/new-extensions-20261023/cast-synonym/`，不纳入 Git。
这些结果证明上述构建和测试路径通过，不代表项目的生产成熟度或仓库发布状态。
