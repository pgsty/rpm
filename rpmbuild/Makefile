#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2024-10-30
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   AGPLv3
#==============================================================#


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
	rm -rf ~/rpmbuild/RPMS/x86_64/scws*.rpm /tmp/pigsty-rpm/RPMS/scws*.rpm
	QA_RPATHS=2 rpmbuild -ba ~/rpmbuild/SPECS/scws.spec

# scws is required when building zhparser
scws-install:
	sudo yum remove -y scws || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/scws-1.2.3-1PIGSTY.el*.x86_64.rpm

#---------------------------------------------#
# libduckdb (deps of duckdb_fdw)
#---------------------------------------------#
libduckdb:
	rm -rf ~/rpmbuild/RPMS/x86_64/libduckdb*.rpm;
	rpmbuild --without debuginfo -ba ~/rpmbuild/SPECS/libduckdb.spec

# scws is required when building zhparser
libduckdb-install:
	sudo yum remove -y libduckdb || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/libduckdb-1.*.el*.x86_64.rpm

#---------------------------------------------#
# pg_filedump (lz4-devel libzstd-devel)
#---------------------------------------------#
pg_filedump:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_filedump*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_filedump.spec


###############################################################
#                      The 1st Batch                          #
###############################################################
batch1: zhparser duckdb_fdw hunspell hydra age age15 pg_tde pgjwt vault supautils index_advisor plv8 pg_duckdb

# depend on scws
zhparser:
	QA_RPATHS=2 ./build zhparser

# depend on libduckdb
duckdb_fdw:
	./build duckdb_fdw 12 13 14 15 16

hunspell:
	./build hunspell_cs_cz
	./build hunspell_de_de
	./build hunspell_en_us
	./build hunspell_fr
	./build hunspell_ne_np
	./build hunspell_nl_nl
	./build hunspell_nn_no
	./build hunspell_pt_pt
	./build hunspell_ru_ru
	./build hunspell_ru_ru_aot

hydra:
	./build hydra 13 14 15 16 #17 not ready yet

age:
	rm -rf ~/rpmbuild/RPMS/x86_64/age*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/age16.spec

age15:
	rm -rf ~/rpmbuild/RPMS/x86_64/age*.rpm;
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

pg_duckdb:
	./build pg_duckdb 15 16 17


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
	aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address quantile lower_quantile pg_timeit pg_random \
	session_variable chkpass pg_currency pg_uri cryptint floatvec pg_auditor noset redis_fdw \
	aggs_for_arrays pg_meta pg_redis_pubsub pg_arraymath pagevis pg_ecdsa pg_cheat_funcs pg_crash pg_math \
	firebird_fdw sequential_uuids pgnodemx pg_hashlib pg_protobuf pg_country pg_fio aws_s3

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
pg_timeit:
	./build pg_timeit
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


###############################################################
#                      The 4th Batch                          #
###############################################################
batch4: geoip plproxy table_version ddlx postgresql_anonymizer kafka_fdw log_fdw pg_mon pgqr pg_zstd pg_geohash acl pg_emailaddr smlar pgmq pg_timeseries pg_plan_filter

# missing packages in PGDG repo (with un-aligned versions)
geoip:
	./build geoip 16 17     # el8/el9
plproxy:
	./build plproxy 16 17   # el8/el9
table_version:
	./build table_version   # el8/el9
ddlx:
	./build toastinfo 17
anon: postgresql_anonymizer
postgresql_anonymizer:
	./build postgresql_anonymizer 17

# missing PG major version
kafka_fdw:
	./build kafka_fdw 12 13 14 15 16
log_fdw:
	./build log_fdw 14 15 16 17
pg_mon:
	./build pg_mon
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
pgsodium:
	./build pgsodium 17
pg4ml:
	./build pg4ml


###############################################################
#               6. RUST / PGRX Extensions                     #
###############################################################
rust1: pg_graphql pg_jsonschema wrappers pg_idkit pgsmcrypto pg_tiktoken pg_summarize pg_polyline pg_explain_ui pg_cardano pg_base58 pg_parquet pg_vectorize pgvectorscale
rust2: pgml plprql pg_later pg_smtp_client
rust3: pgdd

# pgrx 0.12.7
pg_graphql:
	./build pg_graphql nodebug 14 15 16 17
pg_jsonschema:
	./build pg_jsonschema nodebug
wrappers:
	./build wrappers nodebug 14 15 16 17
pg_idkit:
	./build pg_idkit nodebug
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
	./build pg_vectorize nodebug 14 15 16
pgvectorscale:
	./build pgvectorscale nodebug 13 14 15 16 17


# pgrx 0.11.4
pgml:
	./build pgml nodebug 14 15 16 17
plprql:
	./build plprql nodebug 12 13 14 15 16
pg_later:
	./build pg_later nodebug 13 14 15 16
pg_smtp_client:
	./build pg_smtp_client nodebug 14 15 16


# pgrx 0.10.x
pgdd:
	./build pgdd nodebug



###############################################################
#                         Obsolete                            #
###############################################################

pg_search:
	./build pg_search 12 13 14 15 16 17

pg_lakehouse:
	./build pg_search 15 16

pg_analytics:
	./build pg_analytics 15 16 17

pg_tier:
	./build pg_tier 16

libarrow-s3:
	rm -rf ~/rpmbuild/RPMS/x86_64/libarrow-s3*.rpm;
	rpmbuild -ba ~/rpmbuild/SPECS/libarrow-s3.spec

parquet_s3_fdw:
	./build parquet_s3_fdw 16

unit:
	./build unit 16

mysqlcompat:
	./build mysqlcompat 16

sslutils:
	./build sslutils 12 13 14 15 16 17


###############################################################
#                     RPM & SRPM                              #
###############################################################
ls-rpm:
	ls -alh  ~/rpmbuild/RPMS/x86_64/
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
	batch1 zhparser duckdb_fdw hunspell hydra age age15 pg_tde pgjwt vault supautils index_advisor plv8 pg_duckdb \
	batch2 pg_roaringbitmap pg_sqlog pg_hashids postgres_shacrypt permuteseq imgsmlr pg_similarity md5hash preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo \
	batch3 pg_orphaned pgcozy decoder_raw pg_failover_slots pg_financial pg_savior aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address quantile lower_quantile pg_timeit pg_random session_variable chkpass pg_currency pg_uri cryptint floatvec pg_auditor noset redis_fdw \
	aggs_for_arrays pg_meta pg_redis_pubsub pg_arraymath pagevis pg_ecdsa pg_cheat_funcs pg_crash pg_math firebird_fdw sequential_uuids pgnodemx pg_hashlib pg_protobuf pg_country pg_fio aws_s3 \
	batch4 geoip plproxy table_version kafka_fdw log_fdw pg_mon pgqr pg_zstd pg_geohash acl pg_emailaddr smlar pgmq pg_timeseries pg_plan_filter pg_relusage pg_uint128 pg4ml \
	rust pg_search pg_lakehouse pg_graphql pg_jsonschema wrappers pg_vectorize pg_later plprql pg_idkit pgsmcrypto pgvectorscale # pgdd pg_tiktoken pgml pg_parquet pg_polyline pg_explain_ui pg_cardano pg_base58 pg_summarize \
	ls-rpm ls-srpm rm-rpm rm-srpm