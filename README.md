# PGSTY/RPM: build rpm for PostgreSQL Extensions

PostgreSQL Extensions that **NOT** included in the official PGDG repo used by [Pigsty](https://pigsty.io).

Related Projects:

- [`pgsql/pkg`](https://github.com/pgsty/pkg): Infra Packages, PostgreSQL Deps, ParadeDB, DuckDB, etc.
- [`infra_pkg`](https://github.com/pgsty/infra-pkg): Building observability stack & modules from tarball
- [`rpm`](https://github.com/pgsty/rpm): Building PostgreSQL RPM packages from source code
- [`pgsql-deb`](https://github.com/pgsty/pgsql-deb): Building PostgreSQL DEB packages from source code

--------

## What's inside?

41 Extensions build with `c/c++`:

| Extension                                                          | Version     | SPEC                                                            | License                                                                                     | Comment            |
|--------------------------------------------------------------------|-------------|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------|--------------------|
| [scws](https://github.com/hightman/scws)                           | v1.2.3      | [scws.spec](rpmbuild/SPECS/scws.spec)                           | [BSD](https://github.com/hightman/scws/blob/master/COPYING)                                 | Deps of zhparser   |
| [libduckdb](https://github.com/duckdb/duckdb)                      | v1.0.0      | [libduckdb.spec](rpmbuild/SPECS/libduckdb.spec)                 | [MIT](https://github.com/duckdb/duckdb/blob/main/LICENSE)                                   | Deps of duckdb_fdw |
| [pg_filedump](https://github.com/df7cb/pg_filedump)                | v17.0       | [pg_filedump.spec](rpmbuild/SPECS/pg_filedump.spec)             | [GPLv2](https://github.com/df7cb/pg_filedump)                                               |                    |
| [duckdb_fdw](https://github.com/alitrack/duckdb_fdw)               | v1.0.0      | [pg_graphql.spec](rpmbuild/SPECS/duckdb_fdw.spec)               | [MIT](https://github.com/alitrack/duckdb_fdw/blob/main/LICENSE)                             |                    |
| [zhparser](https://github.com/amutu/zhparser)                      | v2.3        | [zhparser.spec](rpmbuild/SPECS/zhparser.spec)                   | [BSD-Like](https://github.com/amutu/zhparser/blob/master/COPYRIGHT)                         |                    |
| [pg_roaringbitmap](https://github.com/ChenHuajun/pg_roaringbitmap) | v0.5.4      | [pg_roaringbitmap.spec](rpmbuild/SPECS/pg_roaringbitmap.spec)   | [Apache-2.0](https://github.com/ChenHuajun/pg_roaringbitmap/blob/master/LICENSE)            |                    |
| [pgjwt](https://github.com/michelp/pgjwt)                          | v0.2.0      | [pgjwt.spec](rpmbuild/SPECS/pgjwt.spec)                         | [MIT](https://github.com/michelp/pgjwt/blob/master/LICENSE)                                 |                    |
| [vault](https://github.com/supabase/vault)                         | v0.2.9      | [vault.spec](rpmbuild/SPECS/vault.spec)                         | [Apache-2.0](https://github.com/supabase/vault/blob/main/LICENSE)                           |                    |
| [hydra](https://github.com/hydradatabase/hydra)                    | v1.1.2      | [hydra.spec](rpmbuild/SPECS/hydra.spec)                         | [AGPLv3](https://github.com/hydradatabase/hydra/blob/main/columnar/LICENSE)                 |                    |
| [age](https://github.com/apache/age)                               | v1.5.0      | [age.spec](rpmbuild/SPECS/age.spec)                             | [Apache-2.0](https://github.com/apache/age/blob/master/LICENSE)                             | 1.4 with PG15      |
| [plv8](https://github.com/plv8/plv8)                               | v3.2.2      | [plv8.spec](rpmbuild/SPECS/plv8)                                | [BSD-Like](https://github.com/plv8/plv8/blob/r3.2/COPYRIGHT)                                |                    |
| [pg_tde](https://github.com/Percona-Lab/pg_tde/tree/1.0.0-beta)    | v1.0.0-beta | [pg_tde.spec](rpmbuild/SPECS/pg_tde)                            | [MIT](https://github.com/Percona-Lab/pg_tde/blob/1.0.0-beta/LICENSE)                        | beta               |
| [md5hash](https://github.com/tvondra/md5hash)                      | v1.0.1      | [md5hash.spec](rpmbuild/SPECS/md5hash)                          | [BSD Like](https://github.com/tvondra/md5hash/blob/master/LICENSE)                          |                    |
| [hunspell](https://github.com/postgrespro/hunspell_dicts)          | v1.0        | [hunspell.spec](rpmbuild/SPECS/hunspell.spec)                   | [PostgreSQL](https://github.com/postgrespro/hunspell_dicts)                                 |                    |
| [pg_sqlog](https://github.com/kouber/pg_sqlog)                     | v1.6        | [pg_sqlog.spec](rpmbuild/SPECS/pg_sqlog.spec)                   | [BSD 3-Clause](https://github.com/kouber/pg_sqlog/blob/master/LICENSE)                      |                    |
| [pg_hashids](https://github.com/iCyberon/pg_hashids)               | v1.3        | [pg_hashids.spec](rpmbuild/SPECS/pg_hashids.spec)               | [MIT](https://github.com/iCyberon/pg_hashids/blob/master/LICENSE)                           |                    |
| [postgres_shacrypt](https://github.com/dverite/postgres-shacrypt)  | v1.1        | [postgres_shacrypt.spec](rpmbuild/SPECS/postgres_shacrypt.spec) | [PostgreSQL](https://github.com/dverite/postgres-shacrypt/blob/master/LICENSE.md)           |                    |
| [permuteseq](https://github.com/dverite/permuteseq)                | v1.2.2      | [permuteseq.spec](rpmbuild/SPECS/permuteseq.spec)               | [PostgreSQL](https://github.com/dverite/permuteseq/blob/master/LICENSE.md)                  |                    |
| [supautils](https://github.com/supabase/supautils)                 | v2.2.1      | [supautils.spec](rpmbuild/SPECS/supautils.spec)                 | [Apache-2.0](https://github.com/supabase/supautils/blob/master/LICENSE)                     |                    |
| [pg_similarity](https://github.com/eulerto/pg_similarity)          | v1.0        | [pg_similarity.spec](rpmbuild/SPECS/pg_similarity.spec)         | [BSD 3-Clause](https://github.com/eulerto/pg_similarity/blob/master/COPYRIGHT)              |                    |
| [imgsmlr](https://github.com/postgrespro/imgsmlr)                  | v1.0        | [imgsmlr.spec](rpmbuild/SPECS/imgsmlr.spec)                     | [PostgreSQL](https://github.com/postgrespro/imgsmlr/blob/master/LICENSE)                    |                    |
| [preprepare](https://github.com/dimitri/preprepare)                | v0.9        | [preprepare.spec](rpmbuild/SPECS/preprepare.spec)               | [BSD](https://github.com/dimitri/preprepare/blob/master/debian/copyright)                   |                    |
| [first_last_agg](https://github.com/wulczer/first_last_agg)        | v0.1.4      | [first_last_agg.spec](rpmbuild/SPECS/first_last_agg.spec)       | [PostgreSQL](https://pgxn.org/dist/first_last_agg/)                                         |                    |
| [pgpcre](https://github.com/petere/pgpcre)                         | v1          | [pgpcre.spec](rpmbuild/SPECS/pgpcre.spec)                       | [PostgreSQL](https://github.com/petere/pgpcre/blob/master/LICENSE)                          |                    |
| [icu_ext](https://github.com/dverite/icu_ext)                      | v1.8.0      | [icu_ext.spec](rpmbuild/SPECS/icu_ext.spec)                     | [PostgreSQL](https://github.com/petere/pgpcre/blob/master/LICENSE)                          |                    |
| [asn1oid](https://github.com/df7cb/pgsql-asn1oid)                  | v1.5        | [asn1oid.spec](rpmbuild/SPECS/asn1oid.spec)                     | [GPLv3](https://github.com/df7cb/pgsql-asn1oid/blob/master/debian/copyright)                |                    |
| [numeral](https://github.com/df7cb/postgresql-numeral)             | v1.3        | [numeral.spec](rpmbuild/SPECS/numeral.spec)                     | [GPLv2+](https://github.com/df7cb/postgresql-numeral/blob/master/debian/copyright)          |                    |
| [pg_rational](https://github.com/begriffs/pg_rational)             | v0.0.2      | [pg_rational.spec](rpmbuild/SPECS/pg_rational.spec)             | [MIT](https://github.com/begriffs/pg_rational/blob/master/LICENSE)                          |                    |
| [q3c](https://github.com/segasai/q3c)                              | v2.0.1      | [q3c.spec](rpmbuild/SPECS/q3c.spec)                             | [GPL 2.0](https://github.com/segasai/q3c/blob/master/COPYING)                               |                    |
| [pgsphere](https://github.com/postgrespro/pgsphere)                | v1.5.1      | [pgsphere.spec](rpmbuild/SPECS/pgsphere.spec)                   | [BSD](https://github.com/postgrespro/pgsphere/blob/master/COPYRIGHT.pg_sphere)              |                    |
| [pgfaceting](https://github.com/cybertec-postgresql/pgfaceting)    | v0.2.0      | [pgfaceting.spec](rpmbuild/SPECS/pgfaceting.spec)               | [BSD](https://github.com/cybertec-postgresql/pgfaceting)                                    |                    |
| [mimeo](https://github.com/omniti-labs/mimeo)                      | v1.5.1      | [mimeo.spec](rpmbuild/SPECS/mimeo.spec)                         | [PostgreSQL](https://github.com/omniti-labs/mimeo?tab=readme-ov-file#license-and-copyright) |                    |
| [tablelog](https://github.com/snaga/tablelog)                      | v0.1        | [tablelog.spec](rpmbuild/SPECS/tablelog.spec)                   | [BSD 2-Clause](https://github.com/snaga/tablelog)                                           |                    |
| [pg_snakeoil](https://github.com/credativ/pg_snakeoil)             | v1.3        | [pg_snakeoil.spec](rpmbuild/SPECS/pg_snakeoil.spec)             | [BSD Like](https://github.com/credativ/pg_snakeoil/blob/master/debian/copyright)            |                    |
| [pgextwlist](https://github.com/dimitri/pgextwlist)                | v1.17       | [pgextwlist.spec](rpmbuild/SPECS/pgextwlist.spec)               | [PostgreSQL](https://github.com/dimitri/pgextwlist?tab=readme-ov-file#licence)              |                    |
| [toastinfo](https://github.com/credativ/toastinfo)                 | v1.4        | [toastinfo.spec](rpmbuild/SPECS/toastinfo.spec)                 | [PostgreSQL](https://github.com/credativ/toastinfo/blob/master/debian/copyright)            |                    |
| [geoip](https://github.com/tvondra/geoip)                          | v0.3.0      | [geoip.spec](rpmbuild/SPECS/geoip.spec)                         | [BSD-Like](https://github.com/tvondra/geoip/blob/master/LICENSE)                            | pg16@el8, pg16@el9 |
| [tableversion](https://github.com/linz/postgresql-tableversion)    | v1.10.3     | [tableversion.spec](rpmbuild/SPECS/tableversion.spec)           | [BSD-Like](https://github.com/linz/postgresql-tableversion/blob/master/LICENSE)             | pg16@el9           |
| [plproxy](https://github.com/plproxy/plproxy)                      | v2.11.0     | [plproxy.spec](rpmbuild/SPECS/plproxy.spec)                     | [BSD-Like](https://github.com/plproxy/plproxy/blob/master/COPYRIGHT)                        | pg16@el8, pg16@el9 |
| [pgmq](https://github.com/tembo-io/pgmq)                           | v1.2.1      | [pgmq.spec](rpmbuild/SPECS/pgmq.spec)                           | [PostgreSQL](https://github.com/tembo-io/pgmq)                                              | 1                  |

Extension build with `pgrx`:

| name           | alias          | version | url                                            | license    | pg_ver              | requires              |
|:---------------|:---------------|:--------|:-----------------------------------------------|:-----------|:--------------------|:----------------------|
| pg_later       | pg_later       | 0.3.0   | https://github.com/tembo-io/pg_later           | PostgreSQL | {17,16,15,14,13}    | {pgmq}                |
| pgml           | pgml           | 2.9.3   | https://github.com/postgresml/postgresml       | MIT        | {16,15,14}          |                       |
| vectorize      | pg_vectorize   | 0.20.0  | https://github.com/tembo-io/pg_vectorize       | PostgreSQL | {17,16,15,14}       | {pg_cron,pgmq,vector} |
| pg_summarize   | pg_summarize   | 0.0.1   | https://github.com/HexaCluster/pg_summarize    | PostgreSQL | {17,16,15,14,13,12} |                       |
| pg_parquet     | pg_parquet     | 0.1.1   | https://github.com/CrunchyData/pg_parquet/     | PostgreSQL | {17,16,15,14}       |                       |
| plprql         | plprql         | 1.0.0   | https://github.com/kaspermarstal/plprql        | Apache-2.0 | {16,15,14,13,12}    |                       |
| pg_polyline    | pg_polyline    | 0.0.1   | https://github.com/yihong0618/pg_polyline      | MIT        | {17,16,15,14,13,12} |                       |
| wrappers       | wrappers       | 0.4.3   | https://github.com/supabase/wrappers           | Apache-2.0 | {17,16,15,14}       |                       |
| pg_graphql     | pg_graphql     | 1.5.9   | https://github.com/supabase/pg_graphql         | Apache-2.0 | {17,16,15,14}       |                       |
| pg_jsonschema  | pg_jsonschema  | 0.3.3   | https://github.com/supabase/pg_jsonschema      | Apache-2.0 | {17,16,15,14,13,12} |                       |
| pg_cardano     | pg_cardano     | 1.0.3   | https://github.com/Fell-x27/pg_cardano         | MIT        | {17,16,15,14,13,12} |                       |
| pg_smtp_client | pg_smtp_client | 0.2.0   | https://github.com/brianpursley/pg_smtp_client | MIT        | {17,16,15,14}       |                       |
| pg_idkit       | pg_idkit       | 0.2.4   | https://github.com/VADOSWARE/pg_idkit          | Apache-2.0 | {17,16,15,14,13,12} |                       |
| pg_base58      | pg_base58      | 0.0.1   | https://github.com/Fell-x27/pg_base58          | MIT        | {17,16,15,14,13,12} |                       |
| pgdd           | pgdd           | 0.5.2   | https://github.com/rustprooflabs/pgdd          | MIT        | {16,15,14,13,12}    |                       |
| explain_ui     | pg_explain_ui  | 0.0.1   | https://github.com/davidgomes/pg-explain-ui    | PostgreSQL | {17,16,15,14,13,12} |                       |
| pg_session_jwt | pg_session_jwt | 0.1.2   | https://github.com/neondatabase/pg_session_jwt | Apache-2.0 | {17,16,15,14}       |                       |
| pgsmcrypto     | pgsmcrypto     | 0.1.0   | https://github.com/zhuobie/pgsmcrypto          | MIT        | {17,16,15,14,13,12} |                       |
| vectorscale    | pgvectorscale  | 0.5.1   | https://github.com/timescale/pgvectorscale     | PostgreSQL | {17,16,15,14,13}    | {vector}              |
| pg_tiktoken    | pg_tiktoken    | 0.0.1   | https://github.com/kelvich/pg_tiktoken         | Apache-2.0 | {17,16,15,14,13,12} |                       |

```bash
make pg_cardano pg_smtp_client pg_idkit pg_base58 pg_explain_ui pg_session_jwt pgsmcrypto pg_tiktoken

rust1: pg_graphql pg_jsonschema wrappers pg_idkit pgsmcrypto pg_tiktoken pg_summarize pg_polyline pg_explain_ui pg_cardano pg_base58 pg_parquet pg_vectorize pgvectorscale
rust2: pgml plprql pg_later pg_smtp_client
```

| Vendor        | Name                                                       | Version | PGRX                                                                                            | License                                                                     | PG Ver            | Deps          |
|---------------|------------------------------------------------------------|---------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------|---------------|
| Supabase      | [pg_graphql](https://github.com/supabase/pg_graphql)       | v1.5.9  | [v0.12.5](https://github.com/supabase/pg_graphql/blob/master/Cargo.toml#L17)                    | [Apache-2.0](https://github.com/supabase/pg_graphql/blob/master/LICENSE)    | 17,16,15          |               |
| Supabase      | [pg_jsonschema](https://github.com/supabase/pg_jsonschema) | v0.3.2  | [v0.12.5](https://github.com/supabase/pg_jsonschema/blob/master/Cargo.toml#L19)                 | [Apache-2.0](https://github.com/supabase/pg_jsonschema/blob/master/LICENSE) | 17,16,15,14,13,12 |               |
| Supabase      | [wrappers](https://github.com/supabase/wrappers)           | v0.4.3  | [v0.12.6](https://github.com/supabase/wrappers/blob/main/Cargo.lock#L4254)                      | [Apache-2.0](https://github.com/supabase/wrappers/blob/main/LICENSE)        | 17,16,15,14       |               |
| TimescaleDB   | [vectorscale](https://github.com/timescale/pgvectorscale)  | v0.3.0  | [v0.12.5](https://github.com/timescale/pgvectorscale/blob/main/pgvectorscale/Cargo.toml#L17)    | [PostgreSQL](https://github.com/timescale/pgvectorscale/blob/main/LICENSE)  | 17,16,15,14,13,12 |               |
| kelvich       | [pg_tiktoken](https://github.com/Vonng/pg_tiktoken)        | v0.0.1  | [v0.12.6](https://github.com/Vonng/pg_tiktoken/blob/main/Cargo.toml)                            | [Apache-2.0](https://github.com/kelvich/pg_tiktoken/blob/main/LICENSE)      | 16,15,14,13,12    |               |
| PostgresML    | [pgml](https://github.com/postgresml/postgresml)           | v2.9.3  | [v0.11.3](https://github.com/postgresml/postgresml/blob/master/pgml-extension/Cargo.lock#L1785) | [MIT](https://github.com/postgresml/postgresml/blob/master/MIT-LICENSE.txt) | 16,15,14          |               |
| Tembo         | [pg_vectorize](https://github.com/tembo-io/pg_vectorize)   | v0.17.0 | [v0.11.3](https://github.com/tembo-io/pg_vectorize/blob/main/extension/Cargo.toml#L24)          | [PostgreSQL](https://github.com/tembo-io/pg_vectorize/blob/main/LICENSE)    | 16,15,14          | pgmq, pg_cron |
| Tembo         | [pg_later](https://github.com/tembo-io/pg_later)           | v0.1.1  | [v0.11.3](https://github.com/tembo-io/pg_later/blob/main/Cargo.toml#L23)                        | [PostgreSQL](https://github.com/tembo-io/pg_later/blob/main/LICENSE)        | 16,15,14,13       | pgmq          |
| kaspermarstal | [plprql](https://github.com/kaspermarstal/plprql)          | v0.1.0  | [v0.11.3](https://github.com/kaspermarstal/plprql/blob/main/Cargo.toml#L21)                     | [Apache-2.0](https://github.com/kaspermarstal/plprql/blob/main/LICENSE)     | 16,15,14,13,12    |               |
| VADOSWARE     | [pg_idkit](https://github.com/VADOSWARE/pg_idkit)          | v0.2.3  | v0.12.5                                                                                         | [Apache-2.0](https://github.com/VADOSWARE/pg_idkit/blob/main/LICENSE)       | 17,16,15,14,13,12 |               |
| pgsmcrypto    | [pgsmcrypto](https://github.com/Vonng/pgsmcrypto)          | v0.1.0  | v0.12.6                                                                                         | [MIT](https://github.com/zhuobie/pgsmcrypto/blob/main/LICENSE)              | 17,16,15,14,13,12 |               |
| rustprooflabs | [pgdd](https://github.com/rustprooflabs/pgdd)              | v0.5.2  | [v0.10.2](https://github.com/rustprooflabs/pgdd/blob/main/Cargo.toml#L25)                       | [MIT](https://github.com/zhuobie/pgsmcrypto/blob/main/LICENSE)              | 16,15,14,13,12    |               |

13 Extensions that is obsolete due to included in PGDG or no longer maintained:

| Extension                                                                   | SPEC    | Comment                     |
|-----------------------------------------------------------------------------|---------|-----------------------------|
| [pg_net](https://github.com/supabase/pg_net)                                | v0.9.2  | PGDG included, N/A in el7   |
| [pg_tle](https://github.com/aws/pg_tle)                                     | v1.3.4  | PGDG included, for el7 only |
| [pg_bigm](https://github.com/pgbigm/pg_bigm)                                | v1.2    | PGDG included, for el7 only |
| [pgsql-http](https://github.com/pramsey/pgsql-http)                         | v1.6.0  | PGDG included, for el7 only |
| [pgsql-gzip](https://github.com/pramsey/pgsql-gzip)                         | v1.0.0  | PGDG included, for el7 only |
| [pg_dirtyread](https://github.com/df7cb/pg_dirtyread)                       | v2.7    | PGDG included, for el7 only |
| [pointcloud](https://github.com/pgpointcloud/pointcloud)                    | v1.2.5  | PGDG included, for el7 only |
| [pg_analytics](https://github.com/paradedb/pg_analytics)                    | v0.6.1  | No longer maintained        |
| [pg_sparse](https://github.com/paradedb/paradedb/tree/dev/pg_sparse)        | v0.6.1  | No longer maintained        |
| [pg_rrule](https://github.com/petropavel13/pg_rrule)                        | v0.2.0  | broken                      |
| [pg_proctab](https://gitlab.com/pg_proctab/pg_proctab)                      | v0.0.10 | broken                      |
| [pg_search](https://github.com/paradedb/paradedb/tree/dev/pg_search)        | v0.8.6  | take over by paradedb       |
| [pg_lakehouse](https://github.com/paradedb/paradedb/tree/dev/pg_lakehouse)  | v0.8.6  | take over by paradedb       |
| [unit](https://github.com/df7cb/postgresql-unit?tab=readme-ov-file#license) | v7.7    | PGDG included               |
| [mysqlcompat](https://github.com/2ndQuadrant/mysqlcompat)                   | v0.0.7  | Obsolete                    |

----------

## Environment

```bash
# launch pigsty 3-node el build envgst
cd ~/pigsty; make clean; make rpm
./node.yml -i files/pigsty/rpmbuild.yml -t node_repo,node_pkg

# create rpmbuild fhs
rpmdev-setuptree

# install ad hoc packages 
sudo yum groupinstall --nobest -y 'Development Tools';    # el8 only logic
sudo cpanm FindBin; perl -MFindBin -e 1                   # el9 only logic 

# push source to el building VM
make ps      # make push-ss (specs & sources)
```

EL 8/9 Building [Recipe](rpmbuild/Makefile):

```bash
make rust deps plv8 batch1 batch2 batch3 batch4 batch5
batch1: zhparser duckdb_fdw hunspell pg_roaringbitmap pgjwt pg_sqlog pg_hashids postgres_shacrypt permuteseq vault supautils imgsmlr pg_similarity hydra age age15 pg_tde md5hash #pg_proctab
batch2: preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pg_rrule pgfaceting mimeo tablelog pg_snakeoil pgextwlist toastinfo
batch3: geoip table_version plproxy unit
batch4: pg_orphaned pgcozy decoder_raw pg_failover_slots log_fdw index_advisor pg_financial pg_savior aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address lower_quantile pg_timeit quantile pg_random session_variable smlar sslutils pg_mon chkpass pg_currency pg_emailaddr pg_uri cryptint floatvec pg_auditor noset redis_fdw
batch5: aggs_for_arrays pgqr pg_zstd url_encode pg_geohash pg_meta pg_redis_pubsub pg_arraymath pagevis pg_ecdsa pg_cheat_funcs acl pg_crash pg_math
```

EL7 Building [Recipe](rpmbuild/Makefile.el7):

```bash
make deps common debian legacy
deps: scws scws-install pg_filedump
batch1: zhparser hunspell pg_roaringbitmap pgjwt pg_sqlog pg_hashids postgres_shacrypt permuteseq vault pointcloud imgsmlr pg_similarity hydra age15 md5hash
batch2: preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo
batch4: pg_orphaned pgcozy decoder_raw pg_failover_slots log_fdw index_advisor pg_financial pg_savior aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address lower_quantile pg_timeit quantile pg_random session_variable smlar sslutils pg_mon chkpass pg_currency pg_emailaddr pg_uri cryptint floatvec pg_auditor noset redis_fdw
batch5: aggs_for_arrays pgqr pg_zstd url_encode pg_geohash pg_meta pg_arraymath pagevis pg_ecdsa pg_cheat_funcs acl pg_crash pg_math sequential_uuids pgnodemx pg_protobuf pg_country pg_fio aws_s3 firebird_fdw # pg_redis_pubsub kafka_fdw pg_hashlib
```

## Patch

```bash
vi src/pgduckdb/scan/postgres_seq_scan.cpp 76GPL
tar -zcf pg_mooncake-0.1.0.tar.gz pg_mooncake-0.1.0
```

--------

## License

Maintainer: Ruohang Feng / [@Vonng](https://vonng.com/en/) ([rh@vonng.com](mailto:rh@vonng.com))

License: [Apache 2.0](LICENSE)
