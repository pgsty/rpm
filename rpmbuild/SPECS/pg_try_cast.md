# pg_try_cast

官方 [v1.0.0](https://github.com/Mazuco/pg_try_cast/releases/tag/v1.0.0) 的 C/PGXS 配方，
PostgreSQL License，PG16–18。包版本为 `1.0.0`，control/SQL 版本为 `1.0`，未修改上游代码。

原始归档 `pg_try_cast-1.0.0.tar.gz` 来自
<https://github.com/Mazuco/pg_try_cast/archive/refs/tags/v1.0.0.tar.gz>，
SHA-256 为 `dc901d8d98c4c49c9fb45c0278b95ab7ae088a5b534714750d037067acad9971`。
权威归档位于 `~/pgsty/repo/ext/src/`。

在 EL builder 中先取源；失败后仅补充这一归档，不填充 macOS 仓库的 `rpmbuild/SOURCES`：

```bash
cd ~/rpmbuild
pig build get pg_try_cast
./dep pg_try_cast 16 17 18
./build pg_try_cast 16 17 18
```

2026-10-23 的代表性验证覆盖 `pgsty/el9a:build`（Rocky Linux 9.8 / aarch64）与
`pgsty/u24a:build`（Ubuntu 24.04.5 noble / arm64）的 PG16、17、18。
RPM 共 9 个二进制包，包括非空 debuginfo 和 debugsource；DEB 共 3 个主包和 3 个 dbgsym。
主包含真实 LLVM bitcode/index，无扩展 llvmjit 子包及 LLVM/Clang 运行依赖。

各目标 PG 的上游 3 项 regression 全通过，覆盖 domain、typmod 和多种输入类型。
两侧 PG17 另验证 hstore 有效/无效输入；`try_cast('###', NULL::regtype)` 仍抛 SQLSTATE
`42601`。该扩展只能处理支持 soft-error 的输入函数，不能承诺吞掉全部转换错误。
扩展为 trusted，不需要 preload。hstore 仅为测试依赖。

已安装包的 builder 中可从源码目录复现回归：

```bash
PGHOST=/tmp PGPORT=5417 PGUSER=postgres make PG_CONFIG=/usr/pgsql-17/bin/pg_config installcheck
```

临时构建、payload、运行测试与产物清单位于
`/Users/vonng/tmp/new-extensions-20261023/cast-synonym/`，不纳入 Git。
这些结果证明上述构建和测试路径通过，不代表项目的生产成熟度或仓库发布状态。
