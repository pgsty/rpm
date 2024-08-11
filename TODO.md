--------

## **TODO**

- libfq https://github.com/ibarwick/libfq/blob/master/INSTALL.md

- firebird_fdw         https://github.com/ibarwick/firebird_fdw            (el8)
- sequential_uuids     https://github.com/tvondra/sequential-uuids         (el8)
- kafka_fdw            https://github.com/adjust/kafka_fdw
- pgnodemx             https://github.com/CrunchyData/pgnodemx
- pg_hashlib           https://github.com/markokr/pghashlib
- pg_protobuf          https://github.com/afiskon/pg_protobuf             (12-15)
- pg_country           https://github.com/adjust/pg-country
- pg_fio               https://github.com/csimsek/pgsql-fio
- aws_s3               https://github.com/chimpler/postgres-aws-s3         (PureSQL)
- pg_fuzzywuzzy        https://github.com/hooopo/pg-fuzzywuzzy             PureSQL
- git_fdw              https://github.com/franckverrot/git_fdw            （libgit2）


INSERT INTO ext.merge (name, url) VALUES
('firebird_fdw'     ,    'https://github.com/ibarwick/firebird_fdw'       ),
('sequential_uuids' ,    'https://github.com/tvondra/sequential-uuids'       ),
('kafka_fdw'        ,    'https://github.com/adjust/kafka_fdw'       ),
('pgnodemx'         ,    'https://github.com/CrunchyData/pgnodemx'       ),
('pg_hashlib'       ,    'https://github.com/markokr/pghashlib'       ),
('pg_protobuf'      ,    'https://github.com/afiskon/pg_protobuf'       ),
('pg_country'       ,    'https://github.com/adjust/pg-country'       ),
('pg_fio'           ,    'https://github.com/csimsek/pgsql-fio'       ),
('aws_s3'           ,    'https://github.com/chimpler/postgres-aws-s3'       ),
('pg_fuzzywuzzy'    ,    'https://github.com/hooopo/pg-fuzzywuzzy'       ),
('git_fdw'          ,    'https://github.com/franckverrot/git_fdw'       );

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