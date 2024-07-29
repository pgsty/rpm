# pgsql-rpm: build rpm for PostgreSQL Extensions

PostgreSQL Extensions that **NOT** included in the official PGDG repo used by [Pigsty](https://pigsty.io).

Related Projects:

- [`pgsql/pkg`](https://github.com/pgsty/pkg): Infra Packages, PostgreSQL Deps, ParadeDB, DuckDB, etc.
- [`infra_pkg`](https://github.com/pgsty/infra-pkg): Building observability stack & modules from tarball
- [`pgsql-rpm`](https://github.com/pgsty/pgsql-rpm): Building PostgreSQL RPM packages from source code
- [`pgsql-deb`](https://github.com/pgsty/pgsql-deb): Building PostgreSQL DEB packages from source code

--------

## What's inside?

38 Extensions build with `c/c++`:

| Extension                                                          | Version     | SPEC                                                            | License                                                                                     | Comment            |
|--------------------------------------------------------------------|-------------|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------|--------------------|
| [scws](https://github.com/hightman/scws)                           | v1.2.3      | [scws.spec](rpmbuild/SPECS/scws.spec)                           |                                                                                             | Deps of zhparser   |
| [libduckdb](https://github.com/duckdb/duckdb)                      | v1.0.0      | [libduckdb.spec](rpmbuild/SPECS/libduckdb.spec)                 |                                                                                             | Deps of duckdb_fdw |
| [pg_filedump](https://github.com/df7cb/pg_filedump)                | v17.0       | [pg_filedump.spec](rpmbuild/SPECS/pg_filedump.spec)             |                                                                                             |                    |
| [duckdb_fdw](https://github.com/alitrack/duckdb_fdw)               | v1.0.0      | [pg_graphql.spec](rpmbuild/SPECS/duckdb_fdw.spec)               |                                                                                             |                    |
| [zhparser](https://github.com/amutu/zhparser)                      | v2.2        | [zhparser.spec](rpmbuild/SPECS/zhparser.spec)                   |                                                                                             |                    |
| [pg_roaringbitmap](https://github.com/ChenHuajun/pg_roaringbitmap) | v0.5.4      | [pg_roaringbitmap.spec](rpmbuild/SPECS/pg_roaringbitmap.spec)   |                                                                                             |                    |
| [pgjwt](https://github.com/michelp/pgjwt)                          | v0.2.0      | [pgjwt.spec](rpmbuild/SPECS/pgjwt.spec)                         |                                                                                             |                    |
| [vault](https://github.com/supabase/vault)                         | v0.2.9      | [vault.spec](rpmbuild/SPECS/vault.spec)                         |                                                                                             |                    |
| [hydra](https://github.com/hydradatabase/)                         | v1.1.2      | [hydra.spec](rpmbuild/SPECS/hydra.spec)                         |                                                                                             |                    |
| [age](https://github.com/apache/age)                               | v1.5.0      | [age.spec](rpmbuild/SPECS/age.spec)                             |                                                                                             | 1.4 with PG15      |
| [plv8](https://github.com/plv8/plv8)                               | v3.2.2      | [plv8.spec](rpmbuild/SPECS/plv8)                                |                                                                                             |                    |
| [pg_tde](https://github.com/Percona-Lab/pg_tde/tree/1.0.0-beta)    | v1.0.0-beta | [pg_tde.spec](rpmbuild/SPECS/pg_tde)                            |                                                                                             |                    |
| [md5hash](https://github.com/tvondra/md5hash)                      | v1.0.1      | [md5hash.spec](rpmbuild/SPECS/md5hash)                          |                                                                                             |                    |
| [hunspell](https://github.com/postgrespro/hunspell_dicts)          | v1.0        | [hunspell.spec](rpmbuild/SPECS/hunspell.spec)                   |                                                                                             |                    |
| [pg_sqlog](https://github.com/kouber/pg_sqlog)                     | v1.6        | [pg_sqlog.spec](rpmbuild/SPECS/pg_sqlog.spec)                   |                                                                                             |                    |
| [pg_proctab](https://gitlab.com/pg_proctab/pg_proctab)             | v0.0.10     | [pg_proctab.spec](rpmbuild/SPECS/pg_proctab.spec)               |                                                                                             |                    |
| [pg_hashids](https://github.com/iCyberon/pg_hashids)               | v1.3        | [pg_hashids.spec](rpmbuild/SPECS/pg_hashids.spec)               |                                                                                             |                    |
| [postgres_shacrypt](https://github.com/dverite/postgres-shacrypt)  | v1.1        | [postgres_shacrypt.spec](rpmbuild/SPECS/postgres_shacrypt.spec) |                                                                                             |                    |
| [permuteseq](https://github.com/dverite/permuteseq)                | v1.2.2      | [permuteseq.spec](rpmbuild/SPECS/permuteseq.spec)               |                                                                                             |                    |
| [supautils](https://github.com/supabase/supautils)                 | v2.2.1      | [supautils.spec](rpmbuild/SPECS/supautils.spec)                 |                                                                                             |                    |
| [pg_similarity](https://github.com/eulerto/pg_similarity)          | v1.0        | [pg_similarity.spec](rpmbuild/SPECS/pg_similarity.spec)         |                                                                                             |                    |
| [imgsmlr](https://github.com/postgrespro/imgsmlr)                  | v1.0        | [imgsmlr.spec](rpmbuild/SPECS/imgsmlr.spec)                     |                                                                                             |                    |
| [preprepare](https://github.com/dimitri/preprepare)                | v0.9        | [preprepare.spec](rpmbuild/SPECS/preprepare.spec)               | [BSD](https://github.com/dimitri/preprepare/blob/master/debian/copyright)                   |                    |
| [first_last_agg](https://github.com/wulczer/first_last_agg)        | v0.1.4      | [first_last_agg.spec](rpmbuild/SPECS/first_last_agg.spec)       | [PostgreSQL](https://pgxn.org/dist/first_last_agg/)                                         |                    |
| [pgpcre](https://github.com/petere/pgpcre)                         | v1          | [pgpcre.spec](rpmbuild/SPECS/pgpcre.spec)                       | [PostgreSQL](https://github.com/petere/pgpcre/blob/master/LICENSE)                          |                    |
| [icu_ext](https://github.com/dverite/icu_ext)                      | v1.8.0      | [icu_ext.spec](rpmbuild/SPECS/icu_ext.spec)                     | [PostgreSQL](https://github.com/petere/pgpcre/blob/master/LICENSE)                          |                    |
| [asn1oid](https://github.com/df7cb/pgsql-asn1oid)                  | v1.5        | [asn1oid.spec](rpmbuild/SPECS/asn1oid.spec)                     | [GPLv3](https://github.com/df7cb/pgsql-asn1oid/blob/master/debian/copyright)                |                    |
| [numeral](https://github.com/df7cb/postgresql-numeral)             | v1.3        | [numeral.spec](rpmbuild/SPECS/numeral.spec)                     | [GPLv2+](https://github.com/df7cb/postgresql-numeral/blob/master/debian/copyright)          |                    |
| [pg_rational](https://github.com/begriffs/pg_rational)             | v0.0.2      | [pg_rational.spec](rpmbuild/SPECS/pg_rational.spec)             | [MIT](https://github.com/begriffs/pg_rational/blob/master/LICENSE)                          |                    |
| [q3c](https://github.com/segasai/q3c)                              | v2.0.1      | [q3c.spec](rpmbuild/SPECS/q3c.spec)                             | [GPL 2.0](https://github.com/segasai/q3c/blob/master/COPYING)                               |                    |
| [pgsphere](https://github.com/postgrespro/pgsphere)                | v1.5.1      | [pgsphere.spec](rpmbuild/SPECS/pgsphere.spec)                   | [BSD](https://github.com/postgrespro/pgsphere/blob/master/COPYRIGHT.pg_sphere)              |                    |
| [pg_rrule](https://github.com/petropavel13/pg_rrule)               | v0.2.0      | [pg_rrule.spec](rpmbuild/SPECS/pg_rrule.spec)                   | [MIT](https://github.com/petropavel13/pg_rrule/blob/master/LICENSE)                         |                    |
| [pgfaceting](https://github.com/cybertec-postgresql/pgfaceting)    | v0.2.0      | [pgfaceting.spec](rpmbuild/SPECS/pgfaceting.spec)               | [BSD](https://github.com/cybertec-postgresql/pgfaceting)                                    |                    |
| [mimeo](https://github.com/omniti-labs/mimeo)                      | v1.5.1      | [mimeo.spec](rpmbuild/SPECS/mimeo.spec)                         | [PostgreSQL](https://github.com/omniti-labs/mimeo?tab=readme-ov-file#license-and-copyright) |                    |
| [tablelog](https://github.com/snaga/tablelog)                      | v0.1        | [tablelog.spec](rpmbuild/SPECS/tablelog.spec)                   | BSD 2-Clause                                                                                |                    |
| [pg_snakeoil](https://github.com/credativ/pg_snakeoil)             | v1.3        | [pg_snakeoil.spec](rpmbuild/SPECS/pg_snakeoil.spec)             | [BSD Like](https://github.com/credativ/pg_snakeoil/blob/master/debian/copyright)            |                    |
| [pgextwlist](https://github.com/dimitri/pgextwlist)                | v1.17       | [pgextwlist.spec](rpmbuild/SPECS/pgextwlist.spec)               | [PostgreSQL](https://github.com/dimitri/pgextwlist?tab=readme-ov-file#licence)              |                    |
| [toastinfo](https://github.com/credativ/toastinfo)                 | v1.4        | [toastinfo.spec](rpmbuild/SPECS/toastinfo.spec)                 | [PostgreSQL](https://github.com/credativ/toastinfo/blob/master/debian/copyright)            |                    |

16 [Rust](RUST.md) Extension build with `pgrx`:

| Vendor        | Name                                                                       | Version | PGRX                                                                                            | License                                                                     | PG Ver         | Deps          |
|---------------|----------------------------------------------------------------------------|---------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|----------------|---------------|
| PostgresML    | [pgml](https://github.com/postgresml/postgresml)                           | v2.9.3  | [v0.11.3](https://github.com/postgresml/postgresml/blob/master/pgml-extension/Cargo.lock#L1785) | [MIT](https://github.com/postgresml/postgresml/blob/master/MIT-LICENSE.txt) | 16,15,14       |               |
| ParadeDB      | [pg_search](https://github.com/paradedb/paradedb/tree/dev/pg_search)       | v0.8.6  | [v0.11.3](https://github.com/paradedb/paradedb/blob/dev/pg_search/Cargo.toml#L36)               | [AGPLv3](https://github.com/paradedb/paradedb/blob/dev/LICENSE)             | 16,15,14,13,12 |               |
| ParadeDB      | [pg_lakehouse](https://github.com/paradedb/paradedb/tree/dev/pg_lakehouse) | v0.8.6  | [v0.11.3](https://github.com/paradedb/paradedb/blob/dev/pg_lakehouse/Cargo.toml#L26)            | [AGPLv3](https://github.com/paradedb/paradedb/blob/dev/LICENSE)             | 16,15          |               |
| Supabase      | [pg_graphql](https://github.com/supabase/pg_graphql)                       | v1.5.7  | [v0.11.3](https://github.com/supabase/pg_graphql/blob/master/Cargo.toml#L17)                    | [Apache-2.0](https://github.com/supabase/pg_graphql/blob/master/LICENSE)    | 16,15          |               |
| Supabase      | [pg_jsonschema](https://github.com/supabase/pg_jsonschema)                 | v0.3.1  | [v0.11.3](https://github.com/supabase/pg_jsonschema/blob/master/Cargo.toml#L19)                 | [Apache-2.0](https://github.com/supabase/pg_jsonschema/blob/master/LICENSE) | 16,15,14,13,12 |               |
| Supabase      | [wrappers](https://github.com/supabase/wrappers)                           | v0.4.1  | [v0.11.3](https://github.com/supabase/wrappers/blob/main/Cargo.lock#L4254)                      | [Apache-2.0](https://github.com/supabase/wrappers/blob/main/LICENSE)        | 16,15,14       |               |
| Tembo         | [pgmq](https://github.com/tembo-io/pgmq)                                   | v1.2.1  | v0.11.3                                                                                         | [PostgreSQL](https://github.com/tembo-io/pgmq)                              | 16,15,14,13,12 |               |
| Tembo         | [pg_vectorize](https://github.com/tembo-io/pg_vectorize)                   | v0.17.0 | v0.11.3                                                                                         | [PostgreSQL](https://github.com/tembo-io/pg_vectorize/blob/main/LICENSE)    | 16,15,14       | pgmq, pg_cron |
| Tembo         | [pg_later](https://github.com/tembo-io/pg_later)                           | v0.1.1  | v0.11.3                                                                                         | [PostgreSQL](https://github.com/tembo-io/pg_later/blob/main/LICENSE)        | 16,15,14,13    | pgmq          |
| VADOSWARE     | [pg_idkit](https://github.com/VADOSWARE/pg_idkit)                          | v0.2.3  | v0.11.3                                                                                         | [Apache-2.0](https://github.com/VADOSWARE/pg_idkit/blob/main/LICENSE)       | 16,15,14,13,12 |               |
| pgsmcrypto    | [pgsmcrypto](https://github.com/zhuobie/pgsmcrypto)                        | v0.1.0  | v0.11.3                                                                                         | [MIT](https://github.com/zhuobie/pgsmcrypto/blob/main/LICENSE)              | 16,15,14,13,12 |               |
| kelvich       | [pg_tiktoken](https://github.com/kelvich/pg_tiktoken)                      | v0.0.1  | [v0.10.2](https://github.com/kelvich/pg_tiktoken/blob/main/Cargo.toml)                          | [Apache-2.0](https://github.com/kelvich/pg_tiktoken/blob/main/LICENSE)      | 16,15,14,13,12 |               |
| rustprooflabs | [pgdd](https://github.com/rustprooflabs/pgdd)                              | v0.5.2  | [v0.10.2](https://github.com/rustprooflabs/pgdd/blob/main/Cargo.toml#L25)                       | [MIT](https://github.com/zhuobie/pgsmcrypto/blob/main/LICENSE)              | 16,15,14,13,12 |               |
| timescale     | [vectorscale](https://github.com/timescale/pgvectorscale)                  | v0.2.0  | [v0.11.4](https://github.com/timescale/pgvectorscale/blob/main/pgvectorscale/Cargo.toml#L17)    | [PostgreSQL](https://github.com/timescale/pgvectorscale/blob/main/LICENSE)  | 16,15,14,13,12 |               |
| kaspermarstal | [plprql](https://github.com/kaspermarstal/plprql)                          | v0.1.0  | [v0.11.4](https://github.com/kaspermarstal/plprql/blob/main/Cargo.toml#L21)                     | [Apache-2.0](https://github.com/kaspermarstal/plprql/blob/main/LICENSE)     | 16,15,14,13,12 |               |

9 Extensions that is obsolete due to included in PGDG or no longer maintained:

| Extension                                                            | SPEC   | Comment                     |
|----------------------------------------------------------------------|--------|-----------------------------|
| [pg_analytics](https://github.com/paradedb/pg_analytics)             | v0.6.1 | No longer maintained        |
| [pg_sparse](https://github.com/paradedb/paradedb/tree/dev/pg_sparse) | v0.6.1 | No longer maintained        |
| [pg_net](https://github.com/supabase/pg_net)                         | v0.9.2 | PGDG included, N/A in el7   |
| [pg_tle](https://github.com/aws/pg_tle)                              | v1.3.4 | PGDG included, for el7 only |
| [pg_bigm](https://github.com/pgbigm/pg_bigm)                         | v1.2   | PGDG included, for el7 only |
| [pgsql-http](https://github.com/pramsey/pgsql-http)                  | v1.6.0 | PGDG included, for el7 only |
| [pgsql-gzip](https://github.com/pramsey/pgsql-gzip)                  | v1.0.0 | PGDG included, for el7 only |
| [pg_dirtyread](https://github.com/df7cb/pg_dirtyread)                | v2.7   | PGDG included, for el7 only |
| [pointcloud](https://github.com/pgpointcloud/pointcloud)             | v1.2.5 | PGDG included, for el7 only |

Notices: `scws`, `libduckdb`, `pg_filedump`, `pgxnclient`, `pg_search` & `pg_lakehouse` are moved
to [`pgsql/pkg`](https://github.com/pgsty/pkg) due to oversize.


----------

## Environment

```bash
# launch pigsty 3-node el build env
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
make deps common debian rust

deps: scws scws-install libduckdb libduckdb-install pg_filedump
common: zhparser duckdb_fdw hunspell pg_roaringbitmap pgjwt pg_sqlog pg_proctab pg_hashids postgres_shacrypt permuteseq	vault supautils imgsmlr pg_similarity hydra age age15 pg_tde md5hash plv8
rust: pg_search pg_lakehouse pg_graphql pg_jsonschema wrappers pgmq pg_vectorize pg_later plprql pg_idkit pgsmcrypto pgvectorscale # pgdd pg_tiktoken pgml
debian: preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pg_rrule pgfaceting mimeo tablelog pg_snakeoil pgextwlist toastinfo

make pgml # el9 (el8 need gcc13)
```

EL7 Building [Recipe](rpmbuild/Makefile.el7):

```bash
make deps common debian legacy

deps: scws scws-install pg_filedump
common: zhparser hunspell pg_roaringbitmap pgjwt pg_sqlog pg_proctab pg_hashids postgres_shacrypt permuteseq vault pointcloud imgsmlr pg_similarity hydra age15 md5hash
debian: preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pg_rrule pgfaceting mimeo tablelog pg_snakeoil pgextwlist toastinfo
legacy: pg_tle pg_bigm pgsql_http pgsql_gzip pg_dirtyread pointcloud
```

--------

## License

Maintainer: Ruohang Feng / [@Vonng](https://vonng.com/en/) ([rh@vonng.com](mailto:rh@vonng.com))

License: [Apache 2.0](LICENSE)
