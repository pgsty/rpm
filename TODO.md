
## TODO

- [x] plv8 3.2.3
- [x] supautils 2.4.0
- [x] icu_ext 1.9.0
- [x] redis_fdw 17
- [x] pg_failover_slots 1.1.0
- [x] agg_for_vecs 1.3.0 with pg16 / 17
- [x] unit 7.7 -> 7.9 (obsolete)
- [x] pg_uri 16 17
- [x] pg_mon 16
- [x] quantile 16 17
- [x] lower_quantile 16 17
- [x] pg_protobuf 16 17
- [x] log_fdw 1.4 pg17
- [x] pg_duckdb to the latest commit
- [x] pgmq 1.4.4
- [x] pg_timeseries 0.1.6 (new)
- [x] pg_idkit 0.2.4
- [x] pg_graphql 1.5.9
- [x] pg_jsonschema 0.3.2
- [x] pgvectorscale 0.3.0
- [x] pgsmcrypto (+17)
- [x] pg_tiktoken (+17)
- [x] wrappers 0.4.2 (pgrx 0.11.3)
- [x] pg_later 0.1.3 (pgrx 0.11.3)
- [x] pg_vectorize 0.18.3 (pgrx 0.11.3)

- plprql 1.0.0 (pgrx 0.11.3)
- 
- pg_vectorize 0.18.3 TBD
- pg_later 0.1.3 TBD


cp obsolete/template-common.spec firebird_fdw.spec
cp obsolete/template-common.spec sequential_uuids.spec
cp obsolete/template-common.spec kafka_fdw.spec
cp obsolete/template-common.spec pgnodemx.spec
cp obsolete/template-common.spec pg_hashlib.spec
cp obsolete/template-common.spec pg_protobuf.spec
cp obsolete/template-common.spec pg_country.spec
cp obsolete/template-common.spec pg_fio.spec
cp obsolete/template-puresql.spec aws_s3.spec
cp obsolete/template-puresql.spec pg_fuzzywuzzy.spec
cp obsolete/template-common.spec git_fdw.spec


open https://github.com/ibarwick/firebird_fdw
open https://github.com/tvondra/sequential-uuids
open https://github.com/adjust/kafka_fdw
open https://github.com/CrunchyData/pgnodemx
open https://github.com/markokr/pghashlib
open https://github.com/afiskon/pg_protobuf
open https://github.com/adjust/pg-country
open https://github.com/csimsek/pgsql-fio
open https://github.com/chimpler/postgres-aws-s3
open https://github.com/hooopo/pg-fuzzywuzzy
open https://github.com/franckverrot/git_fdw       