# Rust 扩展 pgrx 0.20.0 试点

上游版本复核日期为 2026-11-23，构建回执更新至 2026-11-23 07:39（上海）。逐份搜索两仓活跃配方中的 Rust / cargo-pgrx 调用，并只读核对 PGEXT 的版本和供应来源。70 个 PGEXT 活跃项目另加 DEB 保留的 `pg_typescript`。4 个指定暂缓后，试点涉及 67 个构建单元，包括 66 个 RPM 配方和 65 个 DEB 配方。共发现 12 个较新的扩展版本。

## 构建环境

| 主机 | 镜像 | 容器内系统 | 架构 | Rust / cargo-pgrx |
|---|---|---|---|---|
| m5 | `pgsty/el9a:build` | Rocky Linux 9.9 | aarch64 | 1.100.0 / 0.20.0 |
| m3 | `pgsty/u24:build` | Ubuntu 24.04.5 LTS (noble) | amd64 | 1.100.0 / 0.20.0 |

两台容器的 `pg_config` 实测版本均为 15.20、16.16、17.12、18.7 和 19.0。

`包` 表示已完成原生打包和 payload 检查。RPM 核对主包、debuginfo、debugsource、架构、PG 安装路径和运行依赖。DEB 核对主包、dbgsym、PG 安装路径及共享文档路径。`编` 表示该坐标通过锁定依赖的 `cargo check --lib`，原生包尚缺验包回执。构建阶段和首错按具体坐标记录。项目原有 PG 下限高于 15 的，从实际支持的版本开始。PG19 失败时另列上界验证结果。

`pgrx` 0.20.0 的 Cargo 清单要求 Rust ≥ 1.99.1。两台试点均使用 Rust 1.100.0 和已缓存的 Cargo 依赖。原配方或上游源码指定旧版 Rust 或 `stable` 别名时，迁移配方选择经验证的工具链。两个端点之间的 PG 主版本列入配方目标，实际编译和打包覆盖以逐项记录为准。

| 平台 | 应试配方 | 两端均验包的配方 | 端点验包数 / 应试端点 | 全部已验包坐标（含额外 PG） | 仅通过编译检查的坐标 |
|---|---:|---:|---:|---:|---:|
| el9a | 66 | 63 | 126 / 132 | 131 | 0 |
| u24 | 65 | 61 | 122 / 130 | 126 | 0 |

按构建单元去重，63 项在全部适用试点平台验过最低及最高 PG 版本。其中 59 项已在所有适用试点平台验过 PG19。`kafgres`、`lead`、`pg_search`、`stannum` 使用 PG18 作为本轮上限。

共 248 个最低／最高 PG 坐标和 9 个中间坐标通过原生打包及验包。数据库功能测试覆盖 100 个坐标，其中 EL9a 51 个、U24 49 个。

`pgcontext`、`pgml`、`pgvectorscale`、`pg_typescript` 的 pgrx 0.20.0 迁移受阻，首错见[构建记录](#构建记录)。`pg_mooncake`、`pg_tokenizer`、`vchord`、`vchord_bm25` 按要求暂缓。


`pg_base58` 另在两个平台的 PG15 和 PG19 中安装。四个独立数据库实例都成功执行 `CREATE EXTENSION pg_base58`，并通过含前导零的二进制编码、解码往返测试。

| 已安装并运行的扩展 | 已验证坐标 | 数据库检查 |
|---|---|---|
| `pg_statkit` | el9a/PG15、16、17、18、19；u24/PG15、16、17、18、19 | 核对数组均值、空数组和优势比 |
| `pg_when` | el9a/PG15、19；u24/PG15、19 | 在不同会话时区核对纽约时间及秒至纳秒的 Unix 时间戳 |
| `pg_search` | el9a/PG15、18；u24/PG15、18 | BM25 建索引和检索 |
| `pg_warren` | el9a/PG15、19；u24/PG15、19 | 建图、刷新和三节点遍历 |
| `edtf_postgres` | el9a/PG15、19；u24/PG15、19 | 校验 EDTF 季节格式及十年日期区间 |
| `pg_eviltransform` | el9a/PG15、19；u24/PG15、19 | 通过 PostGIS 转换 WGS84 点并核对 GCJ02 的 SRID 和坐标 |
| `pg_pinyin` | el9a/PG15、19；u24/PG15、19 | 中文拼音标量及含 NULL 的批量转换 |
| `pglite_fusion` | el9a/PG15、19；u24/PG15、19 | 在扩展内执行 SQLite 查询并读取整数结果 |
| `pg_table_range` | el9a/PG16、19 | 非分区键剪枝和插入后扩大范围，通过上游的跨会话失效、事务快照及并发写入回归 |
| `pg_mentat` | el9a/PG15、19；u24/PG15、19 | 写入 EDN 属性和实体并用 Datalog 查回 |
| `pg_agent_gate` | el9a/PG18、19；u24/PG18、19 | 预加载扩展并核对 discover 接口 |
| `kafgres` | el9a/PG15、18；u24/PG15、18 | 建立 Kafka 主题并核对分区数 |
| `pg_trickle` | el9a/PG18、19；u24/PG18、19 | 创建流表、EXPLAIN 和增量视图的初始数据 |
| `pgwasm` | el9a/PG15、19；u24/PG15、19 | 上游 WASM add_i32 算术样例 |
| `pg_anon` | el9a/PG15、19；u24/PG15、19 | 安全标签与静态列脱敏 |
| `stannum` | el9a/PG17、18；u24/PG17、18 | 创建索引并执行 ==> 搜索 |
| `plprql` | el9a/PG15、19；u24/PG15、19 | TABLE 与 SETOF 的多行、NULL 和空集 |
| `pg_improv` | el9a/PG15、19；u24/PG15、19 | 可写 CTE 提交后重新计算派生度量 |
| `pgs3` | el9a/PG17、19；u24/PG17、19 | 以 NOLOGIN 服务角色启动 HTTP worker，并核对其 PID、数据库及登录身份 |
| `pg_turbovec` | el9a/PG15、19；u24/PG15、19 | 使用显式 bit_width 建立向量索引，验证索引扫描计划与检索结果 |
| `wrappers` | el9a/PG15、19；u24/PG15、19 | 加载 all_fdws 包并注册 DuckDB、S3 和 Wasm 的 handler 与 validator |
| `pg_parquet` | el9a/PG15、19；u24/PG15、19 | 带引号表名和 SELECT 的 Parquet 文件写读往返 |
| `timescaledb_toolkit` | el9a/PG16、19；u24/PG16、19 | 生成、存储并读取百分位草图 |

`pg_oidc_validator_rust`、`pg_trickle` 另在 U24 使用同一份源码构建树，一次 `make` 生成 PG18、19 两套主包和 dbgsym，逐主版本验包。

深度复核为 43 个 DEB 配方补上并行 make 的执行顺序保护，并核对了全部 61 个迁移配方在 `make -j8` 下的目标顺序，以及 `pg_buildext updatecontrol` 在默认环境生成的包名。另在 U24 通过正常打包入口对 `pg_base58`、`pg_when` 分别一次构建 PG15 和 19，对 `pg_statkit` 一次构建 PG15–19。EL9a 也逐一构建了 `pg_statkit` 的五个主版本。

`wrappers` 在 el9a、u24 的 PG15、19 主包和调试包 build ID 一致。`addr2line` 从调试包将 `s3vec_distance_wrapper` 定位到上游的 Rust 源文件和行号。

el9a 的 `pg_pinyin` PG19、u24 的 `pg_graphql` PG15 还在清除调用端 `RUSTUP_TOOLCHAIN` 后按仓库配方重新打包，主包和调试包通过检查。

U24 另解开 126 个主包及其 dbgsym。128 个共享库和可执行文件均按 build ID 找到匹配的 `.debug_info` 和 `.debug_line`，其中 126 个还带有 `.debug_str_offsets`。

两平台有 126 组相同扩展和 PG 主版本可对照，其中 126 组的 SQL、control、共享库、命令及 PG 安装目录下的数据文件清单一致。清单按发行版安装路径规范化。

EL9a 的 `pgwasm` PG19 在外层命令超时后由原 `rpmbuild` 进程完成。已核对写包与清理日志、SRPM 和三个二进制 RPM 的摘要，并重新验包。

## 上游升级

12 份升版归档均保存在本地源码目录 `~/pgsty/repo/ext/src`。全部通过端点的源码和生效补丁均已校验 SHA256，EL9a 核对 SRPM 文件头，U24 核对构建目录。升版输入覆盖 EL9a 的 24 个端点和 U24 的 24 个端点。`pg_eviltransform`、`pg_pinyin`、`pg_search` 的新版本自带 pgrx 0.20.0 锁文件，验包通过的目标直接使用对应源码。

| 扩展 | 原版本 → 上游 | 源码归档 | 已更新配方 |
|---|---|---|---|
| `edtf_postgres` | 1.3.2 → [1.3.5](https://github.com/monumental-archive/edtf/releases/tag/v1.3.5) | `edtf_postgres-1.3.5.tar.gz` | RPM、DEB |
| `kafgres` | 0.3.2 → [0.3.3](https://github.com/RayElg/kafgres/releases/tag/0.3.3) | `kafgres-0.3.3.tar.gz` | RPM、DEB |
| `pg_agent_gate` | 0.4.1 → [0.4.3](https://github.com/Manuelreyesbravo/pg_agent_gate/releases/tag/v0.4.3) | `pg_agent_gate-0.4.3.tar.gz` | RPM、DEB |
| `pg_eviltransform` | 0.0.7 → [0.0.8](https://github.com/aiyou178/pg_eviltransform/releases/tag/v0.0.8) | `pg_eviltransform-0.0.8.tar.gz` | RPM、DEB |
| `pg_mentat` | 1.20.0 → [1.22.0](https://codeberg.org/gregburd/mentat/src/tag/v1.22.0) | `pg_mentat-1.22.0.tar.gz` | RPM、DEB |
| `pg_parquet` | 0.5.1 → [0.6.1](https://github.com/CrunchyData/pg_parquet/tree/v0.6.1) | `pg_parquet-v0.6.1.tar.gz` | RPM、DEB |
| `pg_pinyin` | 0.0.8 → [0.0.9](https://github.com/aiyou178/pg_pinyin/releases/tag/v0.0.9) | `pg_pinyin-0.0.9.tar.gz` | RPM、DEB |
| `pg_search` | 0.26.6 → [0.27.0](https://github.com/paradedb/paradedb/releases/tag/v0.27.0) | `pg_search-0.27.0.tar.gz` | RPM、DEB |
| `pg_turbovec` | 2.15.0 → [2.16.3](https://codeberg.org/gregburd/pg_turbovec/src/tag/v2.16.3) | `pg_turbovec-2.16.3.tar.gz` | RPM、DEB |
| `pg_when` | 0.1.10 → [0.1.11](https://github.com/frectonz/pg-when/tree/0.1.11) | `pg_when-0.1.11.tar.gz` | RPM、DEB |
| `pglite_fusion` | 0.0.7 → [0.0.8](https://github.com/frectonz/pglite-fusion/tree/v0.0.8) | `pglite-fusion-0.0.8.tar.gz` | RPM、DEB |
| `timescaledb_toolkit` | 1.27.0 → [1.28.0](https://github.com/timescale/timescaledb-toolkit/releases/tag/1.28.0) | `timescaledb-toolkit-1.28.0.tar.gz` | RPM、DEB |

## 逐扩展矩阵

第二列依次给出扫描前版本与上游版本。箭头标记扩展升版，“源码”标记无正式版本标签时从固定提交读取的 Cargo 版本。各配方的 PG 目标、源码与补丁 SHA256、验包回执及首错日志索引见 [JSON 矩阵](rust-pgrx-0.20.0-pilot.json)。

64 项在 PGEXT 的 RPM 和 DEB 供应字段均为 PIGSTY。`encsearch`、`pg_table_range` 仅有活跃 RPM 配方，`pg_typescript` 是 DEB 保留配方。`pgvectorscale` 的 EL9 PG15–18 已有 PGDG 包。

| 扩展 | 原配方 / 上游 | EL9a（PG） | U24（PG） | 已更新配方 | 说明 |
|---|---|---|---|---|---|
| `block_copy_command` | 0.1.5 / [0.1.5](https://github.com/rustwizard/block_copy_command/tree/v0.1.5) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `edtf_postgres` | 1.3.2 → [1.3.5](https://github.com/monumental-archive/edtf/releases/tag/v1.3.5) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `encsearch` | 0.1.1 / [0.1.1](https://github.com/lokeshmulpuru/encsearch/releases/tag/v0.1.1) | 15 包 · 17 包 · 19 包 | 无活跃配方 | RPM | 仅 RPM |
| `etcd_fdw` | 0.0.1 / [0.0.1](https://github.com/cybertec-postgresql/etcd_fdw/releases/tag/v0.0.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `jsonschema` | 0.1.11 / [0.1.11](https://github.com/theory/pg-jsonschema-boon/releases/tag/v0.1.11) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `kafgres` | 0.3.2 → [0.3.3](https://github.com/RayElg/kafgres/releases/tag/0.3.3) | 15 包 · 16 包 · 18 包 · 19 编译失败 | 15 包 · 16 包 · 18 包 · 19 编译失败 | RPM、DEB | PG19 的首错已复现，本轮上限 PG18；PG19 改动涉及逻辑解码元组、事务时间、等待事件与文件接口；见构建记录 |
| `lead` | 1.0.6 / [1.0.6（源码）](https://github.com/planetscale/lead/tree/e3ed2f4ce1388167b0254a0c0c706a61d0a37d83) | 17 包 · 18 包 · 19 编译失败 | 17 包 · 18 包 · 19 编译失败 | RPM、DEB | PG19 的首错已复现，本轮上限 PG18；PG19 移除了 get_relation_info_hook；见构建记录 |
| `pg_agent_gate` | 0.4.1 → [0.4.3](https://github.com/Manuelreyesbravo/pg_agent_gate/releases/tag/v0.4.3) | 18 包 · 19 包 | 18 包 · 19 包 | RPM、DEB | RETURNING OLD/NEW 要求 PG18 起 |
| `pg_anon` | 3.3.2 / [3.3.2](https://gitlab.com/dalibo/postgresql_anonymizer/-/tags/3.3.2) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 适配了关系、元组描述符和系统缓存读取；在释放缓存前复制 relkind |
| `pg_base58` | 0.0.1 / [0.0.1（源码）](https://github.com/Fell-x27/pg_base58/tree/548b9d361e8b89288ee497b55d45e47f7b4ca507) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_bestmatch` | 0.0.2 / [0.0.1](https://github.com/tensorchord/pg_bestmatch.rs/releases/tag/v0.0.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 沿用本地较高版本 |
| `pg_cardano` | 1.2.0 / [1.2.0（源码）](https://github.com/Fell-x27/pg_cardano/tree/5aac863c2fb182fc92f97e6326db3bcba7aded04) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 配方主页 cardano-community 的 v1.2.0 与作者 Fell-x27 的源码指向同一提交 |
| `pg_command_fw` | 0.1.0 / [0.1.0（源码）](https://github.com/rustwizard/pg_command_fw/tree/f577ed4cf86de579bd1e491caa2c6be720c34d17) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_convert` | 0.1.0 / [0.1.0](https://github.com/rustprooflabs/convert/releases/tag/0.1.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_durable` | 0.2.9 / [0.2.9](https://github.com/microsoft/pg_durable/releases/tag/v0.2.9) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_enigma` | 0.5.0 / [0.5.0](https://github.com/SoftwareLibreMx/pg_enigma/releases/tag/pg_enigma-0.5.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_eviltransform` | 0.0.7 → [0.0.8](https://github.com/aiyou178/pg_eviltransform/releases/tag/v0.0.8) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_explain_ui` | 0.0.2 / [0.0.1（源码）](https://github.com/davidgomes/pg-explain-ui/tree/bea4444f6b5f7b4adf7335921f648b4062e2ca8f) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 沿用本地较高版本 |
| `pg_graphql` | 1.6.3 / [1.6.3](https://github.com/supabase/pg_graphql/releases/tag/v1.6.3) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_idkit` | 0.4.0 / [0.4.0](https://github.com/VADOSWARE/pg_idkit/releases/tag/v0.4.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_improv` | 0.14.0 / [0.14.0](https://codeberg.org/gregburd/improv/src/tag/v0.14.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | PG19 的写入目标来自计划的 resultRelationRelids 位图；后台进程使用 pqsignal_be |
| `pg_jsonschema` | 0.3.4 / [0.3.4](https://github.com/supabase/pg_jsonschema/releases/tag/v0.3.4) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_kazsearch` | 2.3.0 / [2.3.0](https://github.com/darkhanakh/pg-kazsearch/releases/tag/v2.3.0) | 16 包 · 19 包 | 16 包 · 19 包 | RPM、DEB | 上游支持范围从 PG16 起 |
| `pg_kv` | 0.1.0 / [0.1.0](https://github.com/Murat7Ay/pg_kv/releases/tag/v0.1.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_later` | 0.4.0 / [0.4.0](https://github.com/ChuckHend/pg_later/releases/tag/v0.4.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_lexo` | 0.6.1 / [0.6.1](https://github.com/Blad3Mak3r/pg_lexo/releases/tag/v0.6.1) | 16 包 · 19 包 | 16 包 · 19 包 | RPM、DEB | 上游 Cargo 的最低 PG feature 为 pg16 |
| `pg_mentat` | 1.20.0 → [1.22.0](https://codeberg.org/gregburd/mentat/src/tag/v1.22.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_money` | 0.3.0 / [0.3.0](https://github.com/RustedBytes/pg-money/releases/tag/v0.3.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_mooncake` | 0.3.0 / [0.3.0](https://github.com/pgsty/pg_mooncake/tree/v0.3.0) | 指定暂缓 | 指定暂缓 | — | 按要求暂缓 |
| `pg_oidc_validator_rust` | 0.1.0 / [0.1.0（源码）](https://github.com/UnAfraid/pg_oidc_validator_rust/tree/b65bbbe288f84fab91d58b8304e8a526d1326af5) | 18 包 · 19 包 | 18 包 · 19 包 | RPM、DEB | OAuth 验证模块使用 PG18 引入的接口 |
| `pg_parquet` | 0.5.1 → [0.6.1](https://github.com/CrunchyData/pg_parquet/tree/v0.6.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 0.6.1 为 tag，最新 Release 为 0.6.0；适配 COPY 的关系和元组描述符、varlena 访问与中断检查；查询形式允许无表名 |
| `pg_pinyin` | 0.0.8 → [0.0.9](https://github.com/aiyou178/pg_pinyin/releases/tag/v0.0.9) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_polyline` | 0.0.1 / [0.0.1（源码）](https://github.com/yihong0618/pg_polyline/tree/4286fc17b26fa3bd66eb491ae98cdc945c6f3fc1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_render` | 0.1.3 / [0.1.3](https://github.com/mkaski/pg_render/releases/tag/v0.1.3) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_rrf` | 0.0.3 / [0.0.3](https://github.com/yuiseki/pg_rrf/releases/tag/v0.0.3) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_search` | 0.26.6 → [0.27.0](https://github.com/paradedb/paradedb/releases/tag/v0.27.0) | 15 包 · 18 包 · 19 适配试编失败 | 15 包 · 18 包 · 19 适配试编失败 | RPM、DEB | PG19 的首错已复现，本轮上限 PG18；0.27.0 上游原包锁定 pgrx 0.20.0；PG19 存储层涉及 Item、缓冲锁及 WAL 接口；见构建记录 |
| `pg_session_jwt` | 0.5.0 / [0.5.0](https://github.com/neondatabase/pg_session_jwt/tree/v0.5.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_smtp_client` | 0.2.1 / [0.2.0](https://github.com/brianpursley/pg_smtp_client/releases/tag/v0.2.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 沿用本地较高版本 |
| `pg_statkit` | 1.1.0 / [1.1.0](https://github.com/kirdmi/pg_statkit/releases/tag/v1.1.0) | 15 包 · 16 包 · 17 包 · 18 包 · 19 包 | 15 包 · 16 包 · 17 包 · 18 包 · 19 包 | RPM、DEB | 已补 PG18 feature，并同步锁定 pgrx-bench；两平台的 PG15–19 均已打包和运行 |
| `pg_strict` | 1.0.5 / [1.0.5](https://github.com/spa5k/pg_strict/releases/tag/v1.0.5) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_summarize` | 0.0.1 / [0.0.0（源码）](https://github.com/HexaCluster/pg_summarize/tree/f72741c8e57e00b0e7a49e50a62530407ec3032e) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 沿用本地较高版本 |
| `pg_table_range` | 0.1.2 / [0.1.2](https://github.com/bitner/pg_table_range/releases/tag/v0.1.2) | 16 包 · 19 包 | 无活跃配方 | RPM | 仅 RPM；上游 Cargo 的最低 PG feature 为 pg16 |
| `pg_tiktoken` | 0.0.1 / [0.0.1（源码）](https://github.com/kelvich/pg_tiktoken/tree/99cb61d1f64b8c4aeb2fe7c5f7839fba54a7ccbf) · 99cb61d | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_tokenizer` | 1.1.0 / [1.1.0](https://github.com/pgsty/pg_tokenizer/tree/v1.1.0) | 指定暂缓 | 指定暂缓 | — | 按要求暂缓 |
| `pg_trickle` | 0.108.3 / [0.108.3](https://github.com/trickle-labs/pg-trickle/releases/tag/v0.108.3) | 18 包 · 19 包 | 18 包 · 19 包 | RPM、DEB | 迁移了解析树节点检查和逻辑解码接口；配方逐 PG 打包 pg_trickle_dump |
| `pg_turbovec` | 2.15.0 → [2.16.3](https://codeberg.org/gregburd/pg_turbovec/src/tag/v2.16.3) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | PG19 的 relopt_parse_elt 没有 PG18 的 isset_offset 字段；索引方法结构由 palloc0 初始化 |
| `pg_typeid` | 0.4.1 / [0.4.1](https://github.com/blitss/typeid-postgres/releases/tag/v0.4.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_tzf` | 0.3.1 / [0.3.1](https://github.com/ringsaturn/pg-tzf/releases/tag/v0.3.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_vectorize` | 0.27.1 / [0.27.1](https://github.com/ChuckHend/pg_vectorize/releases/tag/v0.27.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pg_warren` | 0.8.0 / [0.8.0](https://github.com/ExaDev/pg_warren/releases/tag/v0.8.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | PG19 使用新版命名 DSM 回调及具名 LWLock tranche |
| `pg_when` | 0.1.10 → [0.1.11](https://github.com/frectonz/pg-when/tree/0.1.11) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 0.1.11 取自上游 tag，归档根为 pg-when-0.1.11；上游未提供从 0.1.10 升级的 SQL 脚本 |
| `pgcontext` | 0.3.0 / [0.3.0](https://github.com/evokoa/pgcontext/releases/tag/v0.3.0) | 17 编译失败 · 19 编译失败 | 17 编译失败 · 19 编译失败 | — | U24 的 PG17 / PG19 分别报 61 / 87 个错误，涉及元组指针及规划器；本轮暂缓迁移，等待上游适配；见构建记录 |
| `pgdd` | 0.6.1 / [0.6.1](https://github.com/rustprooflabs/pgdd/releases/tag/0.6.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pggraph` | 1.2.1 / [1.2.1](https://github.com/evokoa/pggraph/releases/tag/v1.2.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pglinter` | 2.0.0 / [2.0.0](https://github.com/pmpetit/pglinter/releases/tag/2.0.0) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pglite_fusion` | 0.0.7 → [0.0.8](https://github.com/frectonz/pglite-fusion/tree/v0.0.8) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 0.0.8 取自上游 tag，GitHub Releases 为空；归档没有上游 SQL 升级脚本 |
| `pgml` | 2.10.0 / [2.10.0](https://github.com/postgresml/postgresml/releases/tag/v2.10.0) | 15 编译失败 · 19 编译失败 | 15 编译失败 · 19 编译失败 | — | 使用锁定子模块、既有 LightGBM 补丁及 python feature；U24 两端在 Aggregate 等接口各报 82 个错误；本轮暂缓迁移，等待上游适配；见构建记录 |
| `pgmqtt` | 0.5.1 / [0.5.1](https://github.com/RayElg/pgmqtt/releases/tag/0.5.1) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pgrdf` | 0.6.40 / [0.6.40](https://github.com/styk-tv/pgRDF/releases/tag/v0.6.40) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pgs3` | 0.1.1 / [0.1.1](https://github.com/pgsty/pgs3/releases/tag/v0.1.1) | 17 包 · 19 包 | 17 包 · 19 包 | RPM、DEB | 上游遗漏 PG19 服务角色连接分支，试点补丁保留原有 NOLOGIN 身份；上游正式下限为 PG17，PG16 为尽力支持 |
| `pgsmcrypto` | 0.1.1 / [0.1.1（源码）](https://github.com/zhuobie/pgsmcrypto/tree/4044419fec20fa0eecf0b626b889c6aaa09fa4ad) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `pgvectorscale` | 0.9.1 / [0.9.1](https://github.com/timescale/pgvectorscale/releases/tag/0.9.1) | 15 编译失败 · 19 编译失败 | 15 编译失败 · 19 编译失败 | — | EL9 的 PG15–18 由 PGDG 供包，本次试编不改变供应来源；索引 AM、varlena 及 ItemPointer 接口需要上游迁移；本轮暂缓迁移，等待上游适配；见构建记录 |
| `pgwasm` | 0.1.0 / [0.1.0（源码）](https://github.com/jnicholls/pgwasm/tree/535b53363f8208af139e757e508e66c46309ee29) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | PG19 适配了共享内存初始化与 ProcedureCreate；试点使用 wasm32-wasip2 |
| `pgx_ulid` | 0.2.3 / [0.2.3](https://github.com/pksunkara/pgx_ulid/releases/tag/v0.2.3) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | — |
| `plprql` | 18.0.2 / [18.0.2](https://github.com/kaspermarstal/plprql/releases/tag/v18.0.2) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 语言处理器改用 PostgreSQL 的逐行 SRF 初始化、返回及收尾宏 |
| `stannum` | 0.1.0 / [0.1.0（源码）](https://github.com/TeamSpringbird/stannum/tree/7573fc49a48486b7acc9a1107545b515ef9a83f3) | 17 包 · 18 包 · 19 编译失败 | 17 包 · 18 包 · 19 编译失败 | RPM、DEB | PG19 的首错已复现，本轮上限 PG18；PG19 涉及规划器 hook、PathKey 和 WAL 页头接口；见构建记录 |
| `timescaledb_toolkit` | 1.27.0 → [1.28.0](https://github.com/timescale/timescaledb-toolkit/releases/tag/1.28.0) | 16 包 · 19 包 | 16 包 · 19 包 | RPM、DEB | 1.28.0 上游最低为 PG16；varlena 序列化和节点检查已适配 pgrx 0.20.0 |
| `vchord` | 1.3.0 / [1.3.0](https://github.com/pgsty/vchord/releases/tag/1.3.0) | 指定暂缓 | 指定暂缓 | — | 按要求暂缓 |
| `vchord_bm25` | 1.1.0 / [1.1.0](https://github.com/pgsty/vchord_bm25/releases/tag/1.1.0) | 指定暂缓 | 指定暂缓 | — | 按要求暂缓 |
| `wrappers` | 0.6.4 / [0.6.4](https://github.com/supabase/wrappers/releases/tag/v0.6.4) | 15 包 · 19 包 | 15 包 · 19 包 | RPM、DEB | 保留 all_fdws，声明 s3vec_distance 依赖上游的 s3vec_type SQL 定义 |
| `pg_typescript` | 0.1.0 / [0.1.0（源码）](https://github.com/isaacd9/pg_typescript/tree/e03ed5460decab37526e129f5577907b972b4898) | 无活跃配方 | 16 准备失败 · 19 准备失败 | — | DEB 保留配方，RPM 已归档；本轮暂缓迁移，等待上游适配；见构建记录 |

## 构建记录

| 扩展 | 坐标 | 首个错误 | 日志（相对 `evidence/`） |
|---|---|---|---|
| `kafgres` | el9a/PG19、u24/PG19 | error[E0425]: cannot find function heap_tuple in this scope | `el9a/revision/kafgres-pg19.log`、`u24/revision/kafgres-pg19.log` |
| `lead` | el9a/PG19、u24/PG19 | error[E0425]: cannot find type get_relation_info_hook_type in module pg_sys | `el9a/sweep/lead-pg19.log`、`u24/sweep/lead-pg19.log` |
| `pg_search` | el9a/PG19、u24/PG19 | error[E0425]: cannot find type Item in module pg_sys | `el9a/revision/pg_search-pg19.log`、`u24/revision/pg_search-pg19.log` |
| `pgcontext` | el9a/PG17、el9a/PG19、u24/PG17、u24/PG19 | error[E0432]: unresolved import pgrx::itemptr::item_pointer_set_all | `el9a/endpoints/pgcontext-pg17.log`、`el9a/endpoints/pgcontext-pg19.log`、`u24/sweep/pgcontext-pg17.log`、`u24/sweep/pgcontext-pg19.log` |
| `pgml` | el9a/PG15、el9a/PG19、u24/PG15、u24/PG19 | error: Aggregate trait must have angle-bracketed generic arguments (e.g., Aggregate<T>). Missing generic argument. | `el9a/revision/pgml-pg15.log`、`el9a/revision/pgml-pg19.log`、`u24/revision/pgml-pg15.log`、`u24/revision/pgml-pg19.log` |
| `pgvectorscale` | el9a/PG15、el9a/PG19、u24/PG15、u24/PG19 | error[E0432]: unresolved import pgrx::set_varsize_4b | `el9a/endpoints/pgvectorscale-pg15.log`、`el9a/endpoints/pgvectorscale-pg19.log`、`u24/sweep/pgvectorscale-pg15.log`、`u24/sweep/pgvectorscale-pg19.log` |
| `stannum` | el9a/PG19、u24/PG19 | error[E0425]: cannot find type get_relation_info_hook_type in module pg_sys | `el9a/revision/stannum-pg19.log`、`u24/revision/stannum-pg19.log` |
| `pg_typescript` | u24/PG16、u24/PG19 | Deno 固定 encoding_rs 0.8.35，pgrx-pg-config 0.20.0 要求 ^0.8.44 | `u24/source/pg_typescript/prepare.log` |

试点包、调试子包及 SRPM 保存在各自容器的 `/pilot/`。本地 `verified-recipes.json` 记录配方使用的补丁 SHA256、PG 目标和对应的验包回执。`evidence/<平台>/review-20261123/` 记录复核时重新构建的包。PGEXT 待同步的内容包括 12 项升版的版本与源码字段，以及已迁移配方的 pgrx 版本和 PG 支持范围。

EL9a 试点后段将容器内 RPM 二进制包的 Zstandard 压缩等级从 19 调至 3，加快大调试包的封装。各包仍使用配方的 release 优化与完整 DWARF，逐包检查主包、debuginfo 和 debugsource。`pg_search` 的 PG19 首错来自为诊断临时启用 `pg19` feature 的源码副本，PG15–18 的打包输入为上游原始归档。

已修复的首错保存在 `~/pgsty/artifacts/rust-pgrx-pilot-20261122/`。`evidence/<平台>/prior-a`、`checks`、`sweep` 保留编译记录，`trial*` 和 `final` 中的 `qa.json` 列出逐包文件和依赖。`inputs/*.json` 记录新源码的来源、归档根和 SHA256。`pg_pinyin` 通过 v0.0.9 的完整 Git tree 逐 blob 核验后重包，`pg_turbovec` 从 Codeberg v2.16.3 归档重包，两份归档均已在两个 builder 解包验证。

`block_copy_command` 的早期错误为 `pgrx::is_a` 被移除，适配使用 `PgNode::is_a_ptr`。`pg_agent_gate` 中五处系统缓存元组读取均先判断空指针，再使用 `GETSTRUCT!`。Ubuntu noble 的 `dwz` 无法解析部分 Rust ELF 的 `.debug_str_offsets`，对应 recipe 保留原始 DWARF 供 `dh_strip` 拆分。

归档配方 `pg_analytics`, `pg_lakehouse`, `pg_tier`, `hyperion_vault` 保持归档。`pg_lakehouse` 的上游主仓版本属于 ParadeDB 当前产品。前次非 Rust 审计另列过 4 项。`hydra` 的列存扩展走 C/PGXS，DEB 配方只在 PATH 中包含 Cargo 目录。独立 Rust 连接池 `pgdog` 两仓为 0.1.63，上游已发布 [0.1.66](https://github.com/pgdogdev/pgdog/releases/tag/v0.1.66)。`neon` 使用自己的 PostgreSQL 内核和私有 ABI。`ivorysql-contrib` 的 Rust 组件是已列入矩阵的 `pgvectorscale` 0.9.1。该组件固定 IvorySQL 5 的 PG18 ABI 和 cargo-pgrx 0.19.2，需随 IvorySQL 单独验证。
