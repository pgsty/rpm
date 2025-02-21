#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2025-02-09
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   AGPLv3
#==============================================================#


ARCH=x86_64

###############################################################
#                        1. Info                              #
###############################################################
default:
	@echo "make <package_name>"


###############################################################
#                         2. Deps                             #
###############################################################
deps: scws scws-install libduckdb libduckdb-install pg_filedump

#---------------------------------------------#
# scws (deps of zhparser)
#---------------------------------------------#
scws:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/scws*.rpm /tmp/pigsty-rpm/RPMS/scws*.rpm
	QA_RPATHS=2 rpmbuild -ba ~/rpmbuild/SPECS/scws.spec

# scws is required when building zhparser
scws-install:
	sudo yum remove -y scws || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/scws-1.2.3-1PIGSTY.el*.$(ARCH).rpm

#---------------------------------------------#
# libduckdb (deps of duckdb_fdw)
#---------------------------------------------#
libduckdb:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/libduckdb*.rpm;
	rpmbuild --without debuginfo -ba ~/rpmbuild/SPECS/libduckdb.spec

# scws is required when building zhparser
libduckdb-install:
	sudo yum remove -y libduckdb || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/libduckdb-1.*.el*.$(ARCH).rpm

#---------------------------------------------#
# pg_filedump (lz4-devel libzstd-devel)
#---------------------------------------------#
pg_filedump:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/pg_filedump*.rpm;
	PATH=/usr/bin:/usr/pgsql-17/bin:$PATH rpmbuild --define "pgmajorversion 17" -ba ~/rpmbuild/SPECS/pg_filedump.spec

###############################################################
#                      The 1st Batch                          #
###############################################################
batch1: zhparser duckdb_fdw hunspell hydra age age15 pg_tde pgjwt vault supautils index_advisor
batch1a: plv8 pg_duckdb pg_mooncake

# depend on scws
zhparser:
	QA_RPATHS=2 ./build zhparser

# depend on libduckdb
duckdb_fdw:
	./build duckdb_fdw

hunspell:
	./build hunspell_cs_cz
	./build hunspell_de_de
	./build hunspell_en_us
	./build hunspell_fr
	./build hunspell_ne_np
	./build hunspell_nl_nl
	./build hunspell_nn_no
	./build hunspell_ru_ru
	./build hunspell_ru_ru_aot
	./build hunspell_pt_pt

hydra:
	./build hydra 13 14 15 16 #17 not ready yet

age:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/age*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/age16.spec

age15:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/age*.rpm;
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/age15.spec

pg_tde:
	./build pg_tde 16

# supabase extensions
pgjwt:
	./build pgjwt nodebug

vault:
	./build vault

supautils:
	./build supautils 13 14 15 16 17

index_advisor:
	./build index_advisor

plv8:
	./build plv8

omnigres:
	./build omnigres
pg_mooncake:
	./build pg_mooncake 14 15 16 17
pg_duckdb:
	./build pg_duckdb 14 15 16 17
pgroonga:
	./build pgroonga 13 14 15 16 17
timescaledb:
	./build timescaledb nodebug 14 15 16 17
citus:
	./build citus nodebug 15 16 17

###############################################################
#                      The 2nd Batch                          #
###############################################################
batch2: pg_roaringbitmap pg_sqlog pg_hashids postgres_shacrypt permuteseq imgsmlr pg_similarity md5hash preprepare first_last_agg \
	pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo

pg_roaringbitmap:
	./build pg_roaringbitmap

pg_sqlog:
	./build pg_sqlog nodebug

pg_hashids:
	./build pg_hashids

postgres_shacrypt:
	./build postgres_shacrypt

permuteseq:
	./build permuteseq

imgsmlr:
	./build imgsmlr

pg_similarity:
	./build pg_similarity

md5hash:
	./build md5hash

preprepare:
	./build preprepare

first_last_agg:
	./build first_last_agg

pgpcre:
	./build pgpcre

icu_ext:
	./build icu_ext

asn1oid:
	./build asn1oid

numeral:
	./build numeral

pg_rational:
	./build pg_rational

q3c:
	./build q3c

pgsphere:
	./build pgsphere

pgfaceting:
	./build pgfaceting

mimeo:
	./build mimeo

table_log:
	./build table_log

pgextwlist:
	./build pgextwlist

toastinfo:
	./build toastinfo



###############################################################
#                      The 3rd Batch                          #
###############################################################
batch3: pg_orphaned pgcozy decoder_raw pg_failover_slots pg_financial pg_savior \
	aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address quantile lower_quantile pg_random \
	session_variable chkpass pg_currency pg_uri cryptint floatvec pg_auditor noset redis_fdw \
	aggs_for_arrays pg_meta pg_redis_pubsub pg_arraymath pagevis url_encode pg_ecdsa pg_cheat_funcs pg_crash pg_math \
	firebird_fdw sequential_uuids pgnodemx pg_hashlib pg_protobuf pg_country pg_fio aws_s3 pg_timeit

pg_orphaned:
	./build pg_orphaned
pgcozy:
	./build pgcozy nodebug
decoder_raw:
	./build decoder_raw
pg_failover_slots:
	./build pg_failover_slots
pg_financial:
	./build pg_financial
pg_savior:
	./build pg_savior 13 14 15 16 17
aggs_for_vecs:
	./build aggs_for_vecs
pg_base36:
	./build pg_base36
pg_base62:
	./build pg_base62
pg_envvar:
	./build pg_envvar
pg_html5_email_address:
	./build pg_html5_email_address
quantile:
	./build quantile
lower_quantile:
	./build lower_quantile
pg_random:
	./build pg_random
session_variable:
	./build session_variable
chkpass:
	./build chkpass
pg_currency:
	./build pg_currency
pg_uri:
	./build pg_uri
cryptint:
	./build cryptint
floatvec:
	./build floatvec
pg_auditor:
	./build pg_auditor
noset:
	./build noset
redis_fdw:
	./build redis_fdw
aggs_for_arrays:
	./build aggs_for_arrays
pg_meta:
	./build pg_meta nodebug
pg_redis_pubsub:
	./build pg_redis_pubsub
pg_arraymath:
	./build pg_arraymath
pagevis:
	./build pagevis
url_encode:
	./build url_encode
pg_ecdsa:
	./build pg_ecdsa
pg_cheat_funcs:
	./build pg_cheat_funcs
pg_crash:
	./build pg_crash
pg_math:
	./build pg_math
firebird_fdw:
	./build firebird_fdw
sequential_uuids:
	./build sequential_uuids
pgnodemx:
	./build pgnodemx
pg_hashlib:
	./build pg_hashlib
pg_protobuf:
	./build pg_protobuf
pg_country:
	./build pg_country
pg_fio:
	./build pg_fio
aws_s3:
	./build aws_s3 nodebug
pg_snakeoil:
	./build pg_snakeoil
pg_timeit:
	./build pg_timeit


###############################################################
#                      The 4th Batch                          #
###############################################################
batch4: geoip plproxy table_version ddlx postgresql_anonymizer count_distinct \
	pg_fkpart pg_store_plan pgcryptokey pgmeminfo pguint temporal_tables sslutils \
	kafka_fdw log_fdw pgqr pg_zstd pg_geohash acl pg_emailaddr smlar pgmq pg_timeseries \
	pg_plan_filter pg_uint128 pg_relusage pg_net pg4ml pgpdf pglogical_ticker pgsodium pg_xenophile

# missing packages in PGDG repo (with un-aligned versions)
geoip:
	./build geoip     # el8/el9
plproxy:
	./build plproxy   # el8/el9
table_version:
	./build table_version   # el8/el9
ddlx:
	./build ddlx
postgresql_anonymizer:
	./build postgresql_anonymizer
count_distinct:
	./build count_distinct
pg_fkpart:
	./build pg_fkpart
pg_store_plan:
	./build pg_store_plan
pgcryptokey:
	./build pgcryptokey
pgmeminfo:
	./build pgmeminfo
pguint:
	./build pguint
temporal_tables:
	./build temporal_tables
sslutils:
	./build sslutils
pglogical_ticker:
	./build pglogical_ticker

# missing PG major version
kafka_fdw:
	./build kafka_fdw 12 13 14 15 16
log_fdw:
	./build log_fdw 14 15 16 17
pgqr:
	./build pgqr
pg_zstd:
	./build pg_zstd
pg_geohash:
	./build pg_geohash
acl:
	./build acl
pg_emailaddr:
	./build pg_emailaddr
smlar:
	./build smlar 13 14 15 16 17
pgmq:
	./build pgmq nodebug
pg_timeseries:
	./build pg_timeseries nodebug
pg_plan_filter:
	./build pg_plan_filter
pg_uint128:
	./build pg_uint128
pg_relusage:
	./build pg_relusage
pg_net:
	./build pg_net
pg4ml:
	./build pg4ml
pgpdf:
	./build pgpdf
pgsodium:
	./build pgsodium 17

omnisketch:
	./build omnisketch
ddsketch:
	./build ddsketch
pg_duration:
	./build pg_duration 17
ddl_historization:
	./build ddl_historization
data_historization:
	./build data_historization
pg_schedoc:
	./build pg_schedoc
floatfile:
	./build floatfile
pg_upless:
	./build pg_upless
vasco:
	./build vasco
pg_xxhash:
	./build pg_xxhash
pg_xenophile:
	./build pg_xenophile
pg_drop_events:
	./build pg_drop_events
documentdb:
	./build documentdb 15 16 17
pg_tracing:
	./build pg_tracing 15 16 17
pg_curl:
	./build pg_curl
pgxicor:
	./build pgxicor
pgsparql:
	./build pgsparql
pgjq:
	./build pgjq 14 15 16 17
hashtypes:
	./build hashtypes 14 15 16 17
db_migrator:
	./build db_migrator
pg_cooldown:
	./build pg_cooldown 13 14 15 16 17
pg_bulkload:
	./build pg_bulkload
pgcollection:
	./build pgcollection 14 15 16 17

pg_bzip:
	./build pg_bzip
pg_http:
	./build pg_http
pg_gzip:
	./build pg_gzip

# not included
logfmt:
	./build logfmt 15 16
pg_kaboom:
	./build pg_kaboom 13 14 15 16
jsonb_apply:
	./build jsonb_apply

###############################################################
#               6. RUST / PGRX Extensions                     #
###############################################################
rust1: pg_graphql pg_jsonschema wrappers pg_idkit pgsmcrypto pg_tiktoken pg_summarize pg_polyline pg_explain_ui pg_cardano pg_base58 pg_parquet pg_vectorize pgvectorscale vchord pglite_fusion pg_bestmatch pg_later pg_smtp_client timescaledb_toolkit
rust2: pgml plprql
rust3: pgdd

rusta: pg_graphql pg_jsonschema wrappers pg_idkit pg_later
rustb: pgsmcrypto pg_tiktoken pg_summarize pg_polyline pg_explain_ui
rustc: pg_cardano pg_base58 pg_parquet pg_vectorize pgvectorscale
rustd: vchord pglite_fusion pg_bestmatch pg_session_jwt pg_smtp_client

# pgrx 0.12.9
pg_graphql:
	./build pg_graphql nodebug 14 15 16 17
pg_jsonschema:
	./build pg_jsonschema nodebug
wrappers:
	./build wrappers nodebug 14 15 16 17
pg_idkit:
	./build pg_idkit nodebug
pg_later:
	./build pg_later nodebug 13 14 15 16 17
pg_anon:
	./build pg_anon nodebug 13 14 15 16 17
timescaledb_toolkit:
	./build timescaledb_toolkit nodebug 14 15 16 17

pgsmcrypto:
	./build pgsmcrypto nodebug
pg_tiktoken:
	./build pg_tiktoken nodebug
pg_summarize:
	./build pg_summarize nodebug
pg_polyline:
	./build pg_polyline nodebug
pg_explain_ui:
	./build pg_explain_ui nodebug
pg_cardano:
	./build pg_cardano nodebug
pg_base58:
	./build pg_base58 nodebug
pg_parquet:
	./build pg_parquet nodebug 14 15 16 17
pg_vectorize:
	./build pg_vectorize nodebug 14 15 16 17
pgvectorscale:
	./build pgvectorscale nodebug 13 14 15 16 17
pg_session_jwt:
	./build pg_session_jwt nodebug 14 15 16 17
pglite_fusion:
	./build pglite_fusion nodebug
pg_bestmatch:
	./build pg_bestmatch nodebug
pg_smtp_client:
	./build pg_smtp_client nodebug 14 15 16 17
pgml:
	./build pgml nodebug 14 15 16 17
vchord:
	./build vchord nodebug 14 15 16 17
vchord_bm25:
	./build vchord_bm25 nodebug 14 15 16 17


# pgrx 0.11.4
plprql:
	./build plprql nodebug 12 13 14 15 16

# pgrx 0.10.x
pgdd:
	./build pgdd nodebug

#prometheus_fdw:
#	./build prometheus_fdw nodebug

###############################################################
#                     RPM & SRPM                              #
###############################################################
ls-rpm:
	ls -alh  ~/rpmbuild/RPMS/$(ARCH)/
ls-srpm:
	ls -alh  ~/rpmbuild/SRPMS/
rm-rpm:
	rm -rf  ~/rpmbuild/RPMS/*
rm-srpm:
	rm -rf  ~/rpmbuild/SRPMS/*


###############################################################
#                      Inventory                              #
###############################################################
.PHONY: default deps scws scws-install libduckdb libduckdb-install \
	deps scws scws-install libduckdb libduckdb-install pg_filedump \
	batch1 zhparser duckdb_fdw hunspell hydra age age15 pg_tde pgjwt vault supautils index_advisor plv8 pg_duckdb pgroonga timescaledb citus omnigres pg_mooncake \
	batch2 pg_roaringbitmap pg_sqlog pg_hashids postgres_shacrypt permuteseq imgsmlr pg_similarity md5hash preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo \
	batch3 pg_orphaned pgcozy decoder_raw pg_failover_slots pg_financial pg_savior aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address quantile lower_quantile pg_timeit pg_random session_variable chkpass pg_currency pg_uri cryptint floatvec pg_auditor noset redis_fdw \
	aggs_for_arrays pg_meta pg_redis_pubsub pg_arraymath pagevis pg_ecdsa pg_cheat_funcs pg_crash pg_math firebird_fdw sequential_uuids pgnodemx pg_hashlib pg_protobuf pg_country pg_fio aws_s3 \
	batch4 geoip plproxy table_version kafka_fdw log_fdw pgqr pg_zstd pg_geohash acl pg_emailaddr smlar pgmq pg_timeseries pg_plan_filter pg_relusage pg_uint128 pg4ml pgpdf pgsodium \
	omnisketch ddsketch pg_duration ddl_historization data_historization pg_schedoc floatfile pg_upless vasco pg_xxhash pg_xenophile pg_drop_events documentdb pg_tracing pg_curl pgxicor pgsparql pgjq hashtypes db_migrator pg_bulkload pg_cooldown pg_mustach jsonb_apply pgcollection pg_bzip \
	rust rust1 rust2 rust3 rusta rustb rustc rustd \
	pg_graphql pg_jsonschema wrappers pg_idkit pgsmcrypto pg_tiktoken pg_summarize pg_polyline pg_explain_ui pg_cardano pg_base58 pg_parquet pg_vectorize timescaledb_toolkit pgvectorscale vchord vchord_bm25 pglite_fusion pg_bestmatch pgml plprql pg_later pg_smtp_client pgdd \
	ls-rpm ls-srpm rm-rpm rm-srpm


