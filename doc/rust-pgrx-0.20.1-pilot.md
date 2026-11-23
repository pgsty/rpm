# Rust 扩展 pgrx 0.20.1 试点

更新于 2026-11-23T16:42:15+08:00（上海时间）。两仓扫描得到 70 个 PGEXT 活跃项目和 DEB 保留的 `pg_typescript`。相比前一轮已更新的配方，本轮没有新增的扩展版本升级。两台原生 builder 均使用 Rust 1.100.0、cargo-pgrx 0.20.1 和 PostgreSQL 15.20、16.16、17.12、18.7、19.0。

| 试点 | 应试配方 | 框架迁移受阻 | 最低和最高 PG 均通过 | PG19 通过 | 原生打包验包 | 完成复核及取包 |
|---|---:|---:|---:|---:|---:|---:|
| m5 · Rocky Linux 9.9 · aarch64 | 66 | 3 | 63 | 61 | 126 / 126 | 126 / 126 |
| m3 · Ubuntu 24.04.5 · amd64 | 65 | 4 | 61 | 59 | 122 / 122 | 122 / 122 |

各扩展在两个试点平台编译其支持的最低和最高主版本。中间版本核对了配方和锁定依赖的 Cargo feature。「通过」要求同时完成原生打包、payload 与依赖检查、构建输入与提交的核对、ELF build-id 与独立 DWARF 配对，以及本地文件的 SHA256 校验。RPM 每个端点包括主包、debuginfo 和 debugsource，DEB 包括主包和 dbgsym。RPM 试点使用 Zstandard 压缩等级 3。

按要求暂缓 `vchord`、`vchord_bm25`、`pg_tokenizer` 和 `pg_mooncake`。`encsearch` 和 `pg_table_range` 仅有活跃 RPM 配方。`pg_typescript` 仅有 DEB 保留配方。`pgdog` 是独立连接池，Neon 和 IvorySQL 属于自带内核的打包流程。历史归档配方沿用[上轮盘点](rust-pgrx-0.20.0-pilot.md)。

## 上游与供应来源

本轮复查了 47 个正式 release、11 个版本标签和 13 个固定提交。上轮已升版的 12 项为 `edtf_postgres`、`kafgres`、`pg_agent_gate`、`pg_eviltransform`、`pg_mentat`、`pg_parquet`、`pg_pinyin`、`pg_search`、`pg_turbovec`、`pg_when`、`pglite_fusion`、`timescaledb_toolkit`。各项目的版本依据及已核验的 ref 见逐项矩阵。工具链使用 [pgrx 0.20.1](https://github.com/pgcentralfoundation/pgrx/releases/tag/v0.20.1)。

PGEXT 的两台试点平台共有 700 个扩展和主版本坐标。EL9a 的 `pgvectorscale` 在 PG15–18 采用 PGDG 的 0.9.1。表中同时给出了该扩展的 pgrx 迁移诊断。两台平台均将 `pg_mentat` 和 `pg_turbovec` 的 PG19 标为缺包。已按目录中的实际二进制版本核对本轮配方的包修订，未发现与两台试点平台的已发布 Pigsty 包修订冲突。

已清理旧 Rust 构建产物 5,232 个，共 27.3 GiB。m1 的恢复副本通过逐文件校验。

已将端点主包与调试包收至本地 `rpm/yum/el9.aarch64/`（378 个 RPM）和 `deb/apt/noble/`（244 个 DEB/DDEB）。PG19 补丁前的 PG18 补充回执单独保存在试点目录。

按最终提交复核了 RPM 快捷目标与 spec 范围（294 个 PG 坐标）及 DEB 生成的 control 包名（285 个 PG 坐标）。两平台的 PGEXT 快照仍将 `kafgres` 和 `lead` 的 PG19 标为 N/A，本轮 PG19 结论来自实际构建和安装。

在 pgrx 0.20.1 下，`pgcontext`、`pgml`、`pgvectorscale` 的最低版本和 PG19 都遇到 API 变更，现有配方分别使用 pgrx 0.19.2、0.12.9、0.19.2。`pg_typescript` 的 DEB 配方使用 0.19.1，迁移在 Deno 的依赖解析阶段受阻。每个试编版本的命令、首错与日志见 JSON。

## 构建矩阵

| 扩展 | 上游版本 | RPM 版本 / DEB 版本 | EL9a | U24 | 依据 |
|---|---|---|---|---|---|
| `block_copy_command` | [0.1.5](https://github.com/rustwizard/block_copy_command/tree/v0.1.5) | 0.1.5 / 0.1.5 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `edtf_postgres` | [1.3.5](https://github.com/monumental-archive/edtf/releases/tag/v1.3.5) | 1.3.5 / 1.3.5 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `encsearch` | [0.1.1](https://github.com/lokeshmulpuru/encsearch/releases/tag/v0.1.1) | 0.1.1 / — | 15 通过、19 通过 | 无活跃配方 | 仅有 RPM 配方 |
| `etcd_fdw` | [0.0.1](https://github.com/cybertec-postgresql/etcd_fdw/releases/tag/v0.0.1) | 0.0.1 / 0.0.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `jsonschema` | [0.1.11](https://github.com/theory/pg-jsonschema-boon/releases/tag/v0.1.11) | 0.1.11 / 0.1.11 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `kafgres` | [0.3.3](https://github.com/RayElg/kafgres/releases/tag/0.3.3) | 0.3.3 / 0.3.3 | 15 通过、19 通过 | 15 通过、19 通过 | PG19 已适配逻辑解码、等待集和段文件读写。已验证变更新旧值、提交时间和重启后的消息读取 |
| `lead` | [1.0.6（源码）](https://github.com/planetscale/lead/commit/e3ed2f4ce1388167b0254a0c0c706a61d0a37d83) | 1.0.6 / 1.0.6 | 17 通过、19 通过 | 17 通过、19 通过 | PG19 已适配 build_simple_rel_hook。已验证搜索数组的顺序扫描、索引、缓存计划和连接 |
| `pg_agent_gate` | [0.4.3](https://github.com/Manuelreyesbravo/pg_agent_gate/releases/tag/v0.4.3) | 0.4.3 / 0.4.3 | 18 通过、19 通过 | 18 通过、19 通过 | 依赖 PG18 起提供的 RETURNING OLD/NEW |
| `pg_anon` | [3.3.2](https://gitlab.com/dalibo/postgresql_anonymizer/-/tags/3.3.2) | 3.3.2 / 3.3.2 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_base58` | [0.0.1（源码）](https://github.com/Fell-x27/pg_base58/commit/548b9d361e8b89288ee497b55d45e47f7b4ca507) | 0.0.1 / 0.0.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_bestmatch` | [0.0.1](https://github.com/tensorchord/pg_bestmatch.rs/releases/tag/v0.0.1) | 0.0.2 / 0.0.2 | 15 通过、19 通过 | 15 通过、19 通过 | 现有配方高于上游最新发布版本，保留配方版本 |
| `pg_cardano` | [1.2.0（源码）](https://github.com/Fell-x27/pg_cardano/commit/5aac863c2fb182fc92f97e6326db3bcba7aded04) | 1.2.0 / 1.2.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_command_fw` | [0.1.0（源码）](https://github.com/rustwizard/pg_command_fw/commit/f577ed4cf86de579bd1e491caa2c6be720c34d17) | 0.1.0 / 0.1.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_convert` | [0.1.0](https://github.com/rustprooflabs/convert/releases/tag/0.1.0) | 0.1.0 / 0.1.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_durable` | [0.2.9](https://github.com/microsoft/pg_durable/releases/tag/v0.2.9) | 0.2.9 / 0.2.9 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_enigma` | [0.5.0](https://github.com/SoftwareLibreMx/pg_enigma/releases/tag/pg_enigma-0.5.0) | 0.5.0 / 0.5.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_eviltransform` | [0.0.8](https://github.com/aiyou178/pg_eviltransform/releases/tag/v0.0.8) | 0.0.8 / 0.0.8 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_explain_ui` | [0.0.1（源码）](https://github.com/davidgomes/pg-explain-ui/commit/bea4444f6b5f7b4adf7335921f648b4062e2ca8f) | 0.0.2 / 0.0.2 | 15 通过、19 通过 | 15 通过、19 通过 | 现有配方高于上游固定提交的 Cargo 版本，保留配方版本 |
| `pg_graphql` | [1.6.3](https://github.com/supabase/pg_graphql/releases/tag/v1.6.3) | 1.6.3 / 1.6.3 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_idkit` | [0.4.0](https://github.com/VADOSWARE/pg_idkit/releases/tag/v0.4.0) | 0.4.0 / 0.4.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_improv` | [0.14.0](https://codeberg.org/gregburd/improv/src/tag/v0.14.0) | 0.14.0 / 0.14.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_jsonschema` | [0.3.4](https://github.com/supabase/pg_jsonschema/releases/tag/v0.3.4) | 0.3.4 / 0.3.4 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_kazsearch` | [2.3.0](https://github.com/darkhanakh/pg-kazsearch/releases/tag/v2.3.0) | 2.3.0 / 2.3.0 | 16 通过、19 通过 | 16 通过、19 通过 | 上游从 PG16 起支持 |
| `pg_kv` | [0.1.0](https://github.com/Murat7Ay/pg_kv/releases/tag/v0.1.0) | 0.1.0 / 0.1.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_later` | [0.4.0](https://github.com/ChuckHend/pg_later/releases/tag/v0.4.0) | 0.4.0 / 0.4.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_lexo` | [0.6.1](https://github.com/Blad3Mak3r/pg_lexo/releases/tag/v0.6.1) | 0.6.1 / 0.6.1 | 16 通过、19 通过 | 16 通过、19 通过 | 上游最早提供 pg16 feature |
| `pg_mentat` | [1.22.0](https://codeberg.org/gregburd/mentat/src/tag/v1.22.0) | 1.22.0 / 1.22.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_money` | [0.3.0](https://github.com/RustedBytes/pg-money/releases/tag/v0.3.0) | 0.3.0 / 0.3.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_mooncake` | [0.3.0](https://github.com/pgsty/pg_mooncake/tree/v0.3.0) | 0.3.0 / 0.3.0 | 按要求暂缓 | 按要求暂缓 | 按要求暂缓 |
| `pg_oidc_validator_rust` | [0.1.0（源码）](https://github.com/UnAfraid/pg_oidc_validator_rust/commit/b65bbbe288f84fab91d58b8304e8a526d1326af5) | 0.1.0 / 0.1.0 | 18 通过、19 通过 | 18 通过、19 通过 | 依赖 PG18 起提供的 OAuth 验证模块接口 |
| `pg_parquet` | [0.6.1](https://github.com/CrunchyData/pg_parquet/tree/v0.6.1) | 0.6.1 / 0.6.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_pinyin` | [0.0.9](https://github.com/aiyou178/pg_pinyin/releases/tag/v0.0.9) | 0.0.9 / 0.0.9 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_polyline` | [0.0.1（源码）](https://github.com/yihong0618/pg_polyline/commit/4286fc17b26fa3bd66eb491ae98cdc945c6f3fc1) | 0.0.1 / 0.0.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_render` | [0.1.3](https://github.com/mkaski/pg_render/releases/tag/v0.1.3) | 0.1.3 / 0.1.3 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_rrf` | [0.0.3](https://github.com/yuiseki/pg_rrf/releases/tag/v0.0.3) | 0.0.3 / 0.0.3 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_search` | [0.27.0](https://github.com/paradedb/paradedb/releases/tag/v0.27.0) | 0.27.0 / 0.27.0 | 15 通过、18 通过 | 15 通过、18 通过 | PG19 的 Item 类型、页缓冲和 WAL 接口需要联合适配 |
| `pg_session_jwt` | [0.5.0](https://github.com/neondatabase/pg_session_jwt/tree/v0.5.0) | 0.5.0 / 0.5.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_smtp_client` | [0.2.0](https://github.com/brianpursley/pg_smtp_client/releases/tag/v0.2.0) | 0.2.1 / 0.2.1 | 15 通过、19 通过 | 15 通过、19 通过 | 现有配方高于上游最新发布版本，保留配方版本 |
| `pg_statkit` | [1.1.0](https://github.com/kirdmi/pg_statkit/releases/tag/v1.1.0) | 1.1.0 / 1.1.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_strict` | [1.0.5](https://github.com/spa5k/pg_strict/releases/tag/v1.0.5) | 1.0.5 / 1.0.5 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_summarize` | [0.0.0（源码）](https://github.com/HexaCluster/pg_summarize/commit/f72741c8e57e00b0e7a49e50a62530407ec3032e) | 0.0.1 / 0.0.1 | 15 通过、19 通过 | 15 通过、19 通过 | 现有配方高于上游固定提交的 Cargo 版本，保留配方版本 |
| `pg_table_range` | [0.1.2](https://github.com/bitner/pg_table_range/releases/tag/v0.1.2) | 0.1.2 / — | 16 通过、19 通过 | 无活跃配方 | 上游最早提供 pg16 feature，仅有 RPM 配方 |
| `pg_tiktoken` | [0.0.1（源码）](https://github.com/kelvich/pg_tiktoken/commit/99cb61d1f64b8c4aeb2fe7c5f7839fba54a7ccbf) | 0.0.1 / 0.0.1+git20260825.99cb61d | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_tokenizer` | [1.1.0](https://github.com/pgsty/pg_tokenizer/tree/v1.1.0) | 1.1.0 / 1.1.0 | 按要求暂缓 | 按要求暂缓 | 按要求暂缓 |
| `pg_trickle` | [0.108.3](https://github.com/trickle-labs/pg-trickle/releases/tag/v0.108.3) | 0.108.3 / 0.108.3 | 18 通过、19 通过 | 18 通过、19 通过 | 配方从 PG18 起构建，包含 pg_trickle_dump |
| `pg_turbovec` | [2.16.3](https://codeberg.org/gregburd/pg_turbovec/src/tag/v2.16.3) | 2.16.3 / 2.16.3 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_typeid` | [0.4.1](https://github.com/blitss/typeid-postgres/releases/tag/v0.4.1) | 0.4.1 / 0.4.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_tzf` | [0.3.1](https://github.com/ringsaturn/pg-tzf/releases/tag/v0.3.1) | 0.3.1 / 0.3.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_vectorize` | [0.27.1](https://github.com/ChuckHend/pg_vectorize/releases/tag/v0.27.1) | 0.27.1 / 0.27.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_warren` | [0.8.0](https://github.com/ExaDev/pg_warren/releases/tag/v0.8.0) | 0.8.0 / 0.8.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_when` | [0.1.11](https://github.com/frectonz/pg-when/tree/0.1.11) | 0.1.11 / 0.1.11 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pgcontext` | [0.3.0](https://github.com/evokoa/pgcontext/releases/tag/v0.3.0) | 0.3.0 / 0.3.0 | 17 / 19 迁移受阻 | 17 / 19 迁移受阻 | pgrx 的元组指针、函数实参和规划器接口发生变化 |
| `pgdd` | [0.6.1](https://github.com/rustprooflabs/pgdd/releases/tag/0.6.1) | 0.6.1 / 0.6.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pggraph` | [1.2.1](https://github.com/evokoa/pggraph/releases/tag/v1.2.1) | 1.2.1 / 1.2.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pglinter` | [2.0.0](https://github.com/pmpetit/pglinter/releases/tag/2.0.0) | 2.0.0 / 2.0.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pglite_fusion` | [0.0.8](https://github.com/frectonz/pglite-fusion/tree/v0.0.8) | 0.0.8 / 0.0.8 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pgml` | [2.10.0](https://github.com/postgresml/postgresml/releases/tag/v2.10.0) | 2.10.0 / 2.10.0 | 15 / 19 迁移受阻 | 15 / 19 迁移受阻 | Aggregate 的泛型、共享内存回调及 GUC 接口需要上游迁移 |
| `pgmqtt` | [0.5.1](https://github.com/RayElg/pgmqtt/releases/tag/0.5.1) | 0.5.1 / 0.5.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pgrdf` | [0.6.40](https://github.com/styk-tv/pgRDF/releases/tag/v0.6.40) | 0.6.40 / 0.6.40 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pgs3` | [0.1.1](https://github.com/pgsty/pgs3/releases/tag/v0.1.1) | 0.1.1 / 0.1.1 | 17 通过、19 通过 | 17 通过、19 通过 | 上游正式支持从 PG17 起 |
| `pgsmcrypto` | [0.1.1（源码）](https://github.com/zhuobie/pgsmcrypto/commit/4044419fec20fa0eecf0b626b889c6aaa09fa4ad) | 0.1.1 / 0.1.1 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pgvectorscale` | [0.9.1](https://github.com/timescale/pgvectorscale/releases/tag/0.9.1) | 0.9.1 / 0.9.1 | 15 / 19 迁移受阻 | 15 / 19 迁移受阻 | varlena、元组指针和索引 AM 接口需要迁移。EL9 的 PG15–18 由 PGDG 供应 |
| `pgwasm` | [0.1.0（源码）](https://github.com/jnicholls/pgwasm/commit/535b53363f8208af139e757e508e66c46309ee29) | 0.1.0 / 0.1.0 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pgx_ulid` | [0.2.3](https://github.com/pksunkara/pgx_ulid/releases/tag/v0.2.3) | 0.2.3 / 0.2.3 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `plprql` | [18.0.2](https://github.com/kaspermarstal/plprql/releases/tag/v18.0.2) | 18.0.2 / 18.0.2 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `stannum` | [0.1.0（源码）](https://github.com/TeamSpringbird/stannum/commit/7573fc49a48486b7acc9a1107545b515ef9a83f3) | 0.1.0 / 0.1.0 | 17 通过、18 通过 | 17 通过、18 通过 | PG19 变更了规划器 hook、PathKey 和 WAL 页头字段 |
| `timescaledb_toolkit` | [1.28.0](https://github.com/timescale/timescaledb-toolkit/releases/tag/1.28.0) | 1.28.0 / 1.28.0 | 16 通过、19 通过 | 16 通过、19 通过 | 上游 1.28.0 从 PG16 起支持 |
| `vchord` | [1.3.0](https://github.com/pgsty/vchord/releases/tag/1.3.0) | 1.3.0 / 1.3.0 | 按要求暂缓 | 按要求暂缓 | 按要求暂缓 |
| `vchord_bm25` | [1.1.0](https://github.com/pgsty/vchord_bm25/releases/tag/1.1.0) | 1.1.0 / 1.1.0 | 按要求暂缓 | 按要求暂缓 | 按要求暂缓 |
| `wrappers` | [0.6.4](https://github.com/supabase/wrappers/releases/tag/v0.6.4) | 0.6.4 / 0.6.4 | 15 通过、19 通过 | 15 通过、19 通过 | — |
| `pg_typescript` | [0.1.0（源码）](https://github.com/isaacd9/pg_typescript/commit/e03ed5460decab37526e129f5577907b972b4898) | — / 0.1.0 | 无活跃配方 | 16 / 19 迁移受阻 | deno_runtime 0.260.0 和 deno_web 0.283.0 均锁定 encoding_rs =0.8.35，pgrx-pg-config 0.20.1 要求 ^0.8.44 |

## 首错与复现

| 扩展 | 平台 / PG | pgrx 0.20.1 首错 |
|---|---|---|
| `kafgres` | el9a / 19（补丁前） | error[E0425]: cannot find function `heap_tuple` in this scope |
| `kafgres` | u24 / 19（补丁前） | error[E0425]: cannot find function `heap_tuple` in this scope |
| `lead` | el9a / 19（补丁前） | error[E0425]: cannot find type `get_relation_info_hook_type` in module `pg_sys` |
| `lead` | u24 / 19（补丁前） | error[E0425]: cannot find type `get_relation_info_hook_type` in module `pg_sys` |
| `pg_search` | el9a / 19 | error[E0425]: cannot find type `Item` in module `pg_sys` |
| `pg_search` | u24 / 19 | error[E0425]: cannot find type `Item` in module `pg_sys` |
| `pgcontext` | el9a / 17 | error[E0432]: unresolved import `pgrx::itemptr::item_pointer_set_all` |
| `pgcontext` | el9a / 19 | error[E0432]: unresolved import `pgrx::itemptr::item_pointer_set_all` |
| `pgcontext` | u24 / 17 | error[E0432]: unresolved import `pgrx::itemptr::item_pointer_set_all` |
| `pgcontext` | u24 / 19 | error[E0432]: unresolved import `pgrx::itemptr::item_pointer_set_all` |
| `pgml` | el9a / 15 | error: `Aggregate` trait must have angle-bracketed generic arguments (e.g., `Aggregate<T>`). Missing generic argument. |
| `pgml` | el9a / 19 | error: `Aggregate` trait must have angle-bracketed generic arguments (e.g., `Aggregate<T>`). Missing generic argument. |
| `pgml` | u24 / 15 | error: `Aggregate` trait must have angle-bracketed generic arguments (e.g., `Aggregate<T>`). Missing generic argument. |
| `pgml` | u24 / 19 | error: `Aggregate` trait must have angle-bracketed generic arguments (e.g., `Aggregate<T>`). Missing generic argument. |
| `pgvectorscale` | el9a / 15 | error[E0432]: unresolved import `pgrx::set_varsize_4b` |
| `pgvectorscale` | el9a / 19 | error[E0432]: unresolved import `pgrx::set_varsize_4b` |
| `pgvectorscale` | u24 / 15 | error[E0432]: unresolved import `pgrx::set_varsize_4b` |
| `pgvectorscale` | u24 / 19 | error[E0432]: unresolved import `pgrx::set_varsize_4b` |
| `stannum` | el9a / 19 | error[E0425]: cannot find type `get_relation_info_hook_type` in module `pg_sys` |
| `stannum` | u24 / 19 | error[E0425]: cannot find type `get_relation_info_hook_type` in module `pg_sys` |
| `pg_typescript` | u24 / 16 | error: failed to select a version for `encoding_rs`. |
| `pg_typescript` | u24 / 19 | error: failed to select a version for `encoding_rs`. |

## 运行验证

| 扩展 | EL9a 已通过 PG | U24 已通过 PG | 实际操作 |
|---|---|---|---|
| `kafgres` | 15、19 | 15、19 | 对照逻辑解码的新旧元组和提交时间，经 Kafka 协议写入、重启并读回 |
| `lead` | 17、19 | 17、19 | 用 SQL 扩展 tin 验证搜索数组、缓存计划和连接 |
| `pg_base58` | 15、19 | 15、19 | 安装、创建扩展并对带前导零的二进制往返编码 |
| `pg_parquet` | 15、19 | 15、19 | 含引号的表名和 SELECT 结果写入 Parquet 并读回 |
| `pg_statkit` | 15、19 | 15、19 | 核对数组均值、空数组和优势比 |
| `wrappers` | 15、19 | 15、19 | 注册 DuckDB、S3、Wasm FDW，验证向量距离 |

`kafgres` 沿用 PG17 起使用的元组、等待集和向量化文件 I/O 分支，并从 PG19 的匿名联合读取提交时间。测试集群启用了 `shared_preload_libraries=kafgres`、`output_plugin_libraries=kafgres`、`wal_level=logical` 和 `track_commit_timestamp=on`。`lead` 在 PG19 改用 `build_simple_rel_hook`，保留前置 hook 调用和基础关系过滤。试点用 `EXPLAIN (FORMAT JSON)` 确认两种执行计划，并对比实际返回行。两项 PG19 适配在 RPM、DEB 各自独立提交。

逐项供应商、锁文件摘要、提交号、包 SHA256、ELF build-id 和诊断命令见[机器可读矩阵](rust-pgrx-0.20.1-pilot.json)。JSON 的 `evidence` 给出本地试点目录，日志和验包回执以该目录为基准。
