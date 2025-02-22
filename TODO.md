## 2025-02-22

- documentdb 0.101-0
- pgcollection (new) 0.9.1
- pg_bzip (new) 1.0.0
- pg_net 0.14.0
- pg_curl 2.4.2
- vault 0.3.1 (become C)
- table_version 1.10.3 -> 1.11.0
- pg_duration 1.0.2
- timescaledb 2.18.2
- pg_analytics 0.3.4
- pg_search 0.15.2
- pg_graphql 1.5.11
- vchord 0.1.1 -> 0.2.1 ((+13))
- vchord_bm25 0.1.0 -> 0.1.1
- pg_mooncake 0.1.1 -> 0.1.2
- pg_duckdb 0.2.0 -> 0.3.1
- pgddl 0.29

```bash
./dep vault
./dep pg_curl

yum install -y libsodium-devel libcurl-devel bzip2-devel jq
apt install libsodium-dev libcurl4-openssl-dev libbz2-dev jq patchelf

make pg_net  # break on el8 u22
make pg_bzip pg_curl pgcollection vault table_version pg_duration ddlx
make pg_graphql vchord_bm25 vchord
make timescaledb
make pg_mooncake
make pg_duckdb
make documentdb
pig b e pgsql_tweaks
```

- pgsql_tweaks 0.11.0




## 2024-12-10
 
- vchord https://github.com/tensorchord/VectorChord 0.1.0 rag    14 -17 (deps)
- pgvectorscale https://github.com/timescale/pgvectorscale/releases/tag/0.5.1 0.5.1 rag
- pg_bestmatch.rs https://github.com/tensorchord/pg_bestmatch.rs 0.0.1 pgrx 0.12.9 rag
- pglite_fusion https://github.com/frectonz/pglite-fusion 0.0.3 type
- pgpdf (depend on libpoppler-glib-dev / poppler-glib-devel) 0.1.0 https://github.com/Florents-Tselai/pgpdf feat
- pg_parquet 0.1.0 -> 0.1.1
- pg_polyline 0.0.1
- pg_cardano 1.0.2 -> 1.0.3
- pg_vectorize 0.20.0
- pg_duckdb 0.1.0 -> 0.2.0
- pg_search 0.13.0 -> 0.13.1 (download)
- aggs_for_vecs 1.3.1 -> 1.3.2

TODO:

- postgresql_anonymizer: https://github.com/daamien/postgresql_anonymizer/tree/latest v2.0-rc2 with rust
- vchord-bm25 TBD: https://github.com/tensorchord/VectorChord-bm25


## 2024-10-20

- [x] plv8 3.2.3
- [x] supautils 2.5.0
- [x] icu_ext 1.9.0
- [x] redis_fdw 17
- [x] pg_failover_slots 1.1.0
- [x] agg_for_vecs 1.3.0 with pg16 / 17
- [x] unit 7.7 -> 7.9 (obsolete)
- [x] pg_uri 16 17 (compile flag)
- [x] pg_mon 16  (compile flag)
- [x] quantile 16 17  (compile flag)
- [x] lower_quantile 16 17  (compile flag)
- [x] pg_protobuf 16 17  (compile flag)
- [x] log_fdw 1.4 pg17
- [x] pg_duckdb to the latest commit
- [x] pg_idkit 0.2.4
- [x] pg_graphql 1.5.9
- [x] pg_jsonschema 0.3.2
- [x] pgvectorscale 0.4.0 (+13,14,17)
- [x] pgsmcrypto (+17)
- [x] pg_tiktoken (+17)
- [x] wrappers 0.4.3 (pgrx 0.12.6)
- [x] pg_later 0.1.3 (pgrx 0.11.3)
- [x] plprql 1.0.0 (pgrx 0.11.3)
- [x] pg_vectorize 0.18.3 (pgrx 0.11.3)

**New Extension**

- [x] pgmq 1.4.4 (from rust to raw SQL)
- [x] pg_timeseries 0.1.6 (new) (mod)
- [x] pg_plan_filter 0.0.1 (new)
- [x] pg_parquet 0.1.0 (pgrx 0.12.6)
- [x] pg_explain_ui https://github.com/davidgomes/pg-explain-ui
- [x] pg_polyline https://github.com/yihong0618/pg_polyline
- [x] pg_cardano https://github.com/Fell-x27/pg_cardano
- [x] pg_base58 https://github.com/Fell-x27/pg_base58
- [x] pg_summarize https://github.com/HexaCluster/pg_summarize
- [x] pg_relusage https://pgxn.org/dist/pg_relusage/0.0.1/

**TBD**

- [ ] upid https://github.com/carderne/upid
- [ ] pg_bestmatch.rs https://github.com/tensorchord/pg_bestmatch.rs
- [ ] pgvector.rs https://github.com/tensorchord/pgvecto.rs
- [ ] pg_stat_sysinfo https://github.com/postgresml/pg_stat_sysinfo
- [ ] pg-jsonschema-boon : https://github.com/tembo-io/pg-jsonschema-boon

- [ ] pg_xenophile https://github.com/bigsmoke/pg_xenophile
- [ ] pg_uint128 https://github.com/pg-uint/pg-uint128 (el8 failed)
- [ ] pg_task https://github.com/RekGRpth/pg_task
- [ ] pg_mustach https://github.com/RekGRpth/pg_mustach
- [ ] graph_component https://api.pgxn.org/src/graph_component/
- [ ] pg_cld2 https://github.com/hedges333/pg_cld2
- [ ] pg_readme https://github.com/bigsmoke/pg_readme
