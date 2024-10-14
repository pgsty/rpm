#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2024-10-14
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
	sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/libduckdb-1.0.0-1PIGSTY.el*.x86_64.rpm

#---------------------------------------------#
# pg_filedump (lz4-devel libzstd-devel)
#---------------------------------------------#
pg_filedump:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_filedump*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_filedump.spec


###############################################################
#                      The 1st Batch                          #
###############################################################
batch1: zhparser duckdb_fdw hunspell pg_roaringbitmap pgjwt pg_sqlog pg_hashids postgres_shacrypt \
	permuteseq vault supautils imgsmlr pg_similarity hydra age age15 pg_tde md5hash

#---------------------------------------------#
# zhparser (depend on scws)
#---------------------------------------------#
zhparser:
	QA_RPATHS=2 ./build zhparser

#---------------------------------------------#
# duckdb_fdw (depend on libduckdb)
#---------------------------------------------#
duckdb_fdw:
	./build duckdb_fdw

#---------------------------------------------#
# pg_duckdb
#---------------------------------------------#
pg_duckdb:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_duckdb*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_duckdb.spec

#---------------------------------------------#
# plv8 (manually build)
#---------------------------------------------#
plv8:
	./build plv8 12 13 14 15 16 #17

#---------------------------------------------#
# hunspell
#---------------------------------------------#
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

#---------------------------------------------#
# pg_roaringbitmap
#---------------------------------------------#
pg_roaringbitmap:
	./build pg_roaringbitmap

#---------------------------------------------#
# pgjwt
#---------------------------------------------#
pgjwt:
	./build pgjwt nodebug

#---------------------------------------------#
# pg_sqlog
#---------------------------------------------#
pg_sqlog:
	./build pg_sqlog nodebug

#---------------------------------------------#
# pg_hashids
#---------------------------------------------#
pg_hashids:
	./build pg_hashids

#---------------------------------------------#
# postgres_shacrypt
#---------------------------------------------#
postgres_shacrypt:
	./build postgres_shacrypt

#---------------------------------------------#
# permuteseq
#---------------------------------------------#
permuteseq:
	./build permuteseq

#---------------------------------------------#
# vault
#---------------------------------------------#
vault:
	./build vault

#---------------------------------------------#
# supautils
#---------------------------------------------#
supautils:
	./build supautils 13 14 15 16 17

#---------------------------------------------#
# imgsmlr
#---------------------------------------------#
imgsmlr:
	./build imgsmlr


#---------------------------------------------#
# pg_similarity
#---------------------------------------------#
pg_similarity:
	./build pg_similarity

#---------------------------------------------#
# hydra (lz4-devel libzstd-devel)
#---------------------------------------------#
hydra:
	./build hydra 13 14 15 16 # 17 not ready yet

#---------------------------------------------#
# apache-age  (dnf install perl perl-FindBin)
# yum install gcc glibc glib-common readline readline-devel zlib zlib-devel flex bison
#---------------------------------------------#
age:
	rm -rf ~/rpmbuild/RPMS/x86_64/age*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/age16.spec

age15:
	rm -rf ~/rpmbuild/RPMS/x86_64/age*.rpm;
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/age15.spec

#---------------------------------------------#
# pg_tde
#---------------------------------------------#
pg_tde:
	./build pg_tde 16

#---------------------------------------------#
# md5hash
#---------------------------------------------#
md5hash:
	./build md5hash



###############################################################
#                      The 2nd Batch                          #
###############################################################
# this batch is migrated from debian APT repo

batch2: preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational \
	q3c pgsphere pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo # pg_rrule

#---------------------------------------------#
# preprepare
#---------------------------------------------#
preprepare:
	./build preprepare

#---------------------------------------------#
# first_last_agg
#---------------------------------------------#
first_last_agg:
	./build first_last_agg

#---------------------------------------------#
# pgpcre
#---------------------------------------------#
pgpcre:
	./build pgpcre

#---------------------------------------------#
# icu_ext
#---------------------------------------------#
icu_ext:
	./build icu_ext

#---------------------------------------------#
# asn1oid
#---------------------------------------------#
asn1oid:
	./build asn1oid

#---------------------------------------------#
# numeral
#---------------------------------------------#
numeral:
	./build numeral

#---------------------------------------------#
# pg_rational
#---------------------------------------------#
pg_rational:
	./build pg_rational

#---------------------------------------------#
# q3c
#---------------------------------------------#
q3c:
	./build q3c

#---------------------------------------------#
# pgsphere
#---------------------------------------------#
pgsphere:
	./build pgsphere

#---------------------------------------------#
# pgfaceting
#---------------------------------------------#
pgfaceting:
	./build pgfaceting

#---------------------------------------------#
# mimeo
#---------------------------------------------#
mimeo:
	./build mimeo

#---------------------------------------------#
# table_log
#---------------------------------------------#
table_log:
	./build table_log

#---------------------------------------------#
# pg_snakeoil
#---------------------------------------------#
pg_snakeoil:
	./build pg_snakeoil


#---------------------------------------------#
# pgextwlist
#---------------------------------------------#
pgextwlist:
	./build pgextwlist

#---------------------------------------------#
# toastinfo
#---------------------------------------------#
toastinfo:
	./build toastinfo


###############################################################
#                      The 3rd Batch                          #
###############################################################
# the third batch is missing packages in PGDG repo (with un-aligned versions)

batch3: geoip table_version plproxy unit

#---------------------------------------------#
# geoip (pg16@el8/el9)
#---------------------------------------------#
geoip:
	rm -rf ~/rpmbuild/RPMS/x86_64/geoip*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/geoip.spec

#---------------------------------------------#
# tableversion (pg15@el7, pg16@el9)
#---------------------------------------------#
table_version:
	rm -rf ~/rpmbuild/RPMS/x86_64/table_version*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/table_version.spec

#---------------------------------------------#
# plproxy (pg16 @ el8/el9)
#---------------------------------------------#
plproxy:
	rm -rf ~/rpmbuild/RPMS/x86_64/plproxy*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/plproxy.spec



###############################################################
#                      The 4th Batch                          #
###############################################################
batch4: pg_orphaned pgcozy decoder_raw pg_failover_slots log_fdw index_advisor pg_financial pg_savior \
	aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address lower_quantile pg_timeit quantile pg_random \
	session_variable smlar pg_mon chkpass pg_currency pg_emailaddr pg_uri cryptint floatvec pg_auditor noset redis_fdw

pg_orphaned:
	./build pg_orphaned
pgcozy:
	./build pgcozy nodebug
decoder_raw:
	./build decoder_raw
pg_failover_slots:
	./build pg_failover_slots 12 13 14 15 16 #17
log_fdw:
	./build log_fdw 14 15 16  #17
index_advisor:
	./build index_advisor nodebug
pg_financial:
	./build pg_financial
pg_savior:
	./build pg_savior
aggs_for_vecs:
	./build aggs_for_vecs 12 13 14 15
pg_base36:
	./build pg_base36
pg_base62:
	./build pg_base62
pg_envvar:
	./build pg_envvar
pg_html5_email_address:
	./build pg_html5_email_address
lower_quantile:
	./build lower_quantile 12 13 14 15
pg_timeit:
	./build pg_timeit
quantile:
	./build quantile 12 13 14 15
pg_random:
	./build pg_random
session_variable:
	./build session_variable
smlar:
	./build smlar 13 14 15
pg_mon:
	./build pg_mon 12 13 14 15
chkpass:
	./build chkpass
pg_currency:
	./build pg_currency
pg_emailaddr:
	./build pg_emailaddr 12 13 14 15
pg_uri:
	./build pg_uri 12 13 14 15
cryptint:
	./build cryptint
floatvec:
	./build floatvec
pg_auditor:
	./build pg_auditor nodebug
noset:
	./build noset
redis_fdw:
	./build redis_fdw


###############################################################
#                   5th Batch Extension                       #
###############################################################
batch5: aggs_for_arrays pgqr pg_zstd url_encode pg_geohash pg_meta pg_redis_pubsub \
	pg_arraymath pagevis pg_ecdsa pg_cheat_funcs acl pg_crash pg_math \
	sequential_uuids kafka_fdw pgnodemx pg_hashlib pg_protobuf pg_country pg_fio aws_s3 firebird_fdw

aggs_for_arrays:
	./build aggs_for_arrays
pgqr:
	./build pgqr 12 13 14 15
pg_zstd:
	./build pg_zstd 12 13 14 15
url_encode:
	./build url_encode
pg_geohash:
	./build pg_geohash 12 13 14 15
pg_meta:
	./build pg_meta nodebug
pg_redis_pubsub:
	./build pg_redis_pubsub
pg_arraymath:
	./build pg_arraymath
pagevis:
	./build pagevis
pg_ecdsa:
	./build pg_ecdsa
pg_cheat_funcs:
	./build pg_cheat_funcs
acl:
	./build acl 12 13 14 15
pg_crash:
	./build pg_crash
pg_math:
	./build pg_math
firebird_fdw:
	./build firebird_fdw
sequential_uuids:
	./build sequential_uuids
kafka_fdw:
	./build kafka_fdw
pgnodemx:
	./build pgnodemx 12 13 14 15 16 #17
pg_hashlib:
	./build pg_hashlib
pg_protobuf:
	./build pg_protobuf 12 13 14 15
pg_country:
	./build pg_country
pg_fio:
	./build pg_fio
aws_s3:
	./build aws_s3 nodebug


###############################################################
#               4. RUST / PGRX Extensions                     #
###############################################################
rust: pg_search pg_lakehouse pg_graphql pg_jsonschema wrappers pgmq pg_vectorize pg_later plprql pg_idkit pgsmcrypto pgvectorscale
# pgdd pg_tiktoken # pgml

#---------------------------------------------#
# pgml [RUST]
#---------------------------------------------#
pgml:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgml*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgml.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgml.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgml.spec

#---------------------------------------------#
# pg_graphql [RUST]
#---------------------------------------------#
pg_graphql:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_graphql*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 17" -ba ~/rpmbuild/SPECS/pg_graphql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_graphql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_graphql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_graphql.spec

#---------------------------------------------#
# pg_jsonschema [RUST]
#---------------------------------------------#
pg_jsonschema:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_jsonschema*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 17" -ba ~/rpmbuild/SPECS/pg_jsonschema.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_jsonschema.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_jsonschema.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_jsonschema.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_jsonschema.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_jsonschema.spec

#---------------------------------------------#
# wrappers [RUST]
#---------------------------------------------#
wrappers:
	rm -rf ~/rpmbuild/RPMS/x86_64/wrappers*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/wrappers.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/wrappers.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/wrappers.spec

#---------------------------------------------#
# pgmq [RUST]
#---------------------------------------------#
pgmq:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgmq*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgmq.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgmq.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgmq.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgmq.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgmq.spec

#---------------------------------------------#
# pg_vectorize [RUST]
#---------------------------------------------#
pg_vectorize:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_vectorize*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_vectorize.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_vectorize.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_vectorize.spec

#---------------------------------------------#
# pg_later [RUST]
#---------------------------------------------#
pg_later:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_later*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_later.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_later.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_later.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_later.spec

#---------------------------------------------#
# plprql [RUST]
#---------------------------------------------#
plprql:
	rm -rf ~/rpmbuild/RPMS/x86_64/plprql*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/plprql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/plprql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/plprql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/plprql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/plprql.spec

#---------------------------------------------#
# pg_idkit [RUST]
#---------------------------------------------#
pg_idkit:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_idkit*.rpm;
	rm -rf ~/rpmbuild/RPMS/x86_64/plprql*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_idkit.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_idkit.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_idkit.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_idkit.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_idkit.spec

#---------------------------------------------#
# pgsmcrypto [RUST]
#---------------------------------------------#
pgsmcrypto:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgsmcrypto*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgsmcrypto.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgsmcrypto.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgsmcrypto.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgsmcrypto.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgsmcrypto.spec

#---------------------------------------------#
# pgvectorscale [RUST]
#---------------------------------------------#
pgvectorscale:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgvectorscale*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgvectorscale.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgvectorscale.spec

#---------------------------------------------#
# pgdd [RUST]
#---------------------------------------------#
pgdd:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgdd*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgdd.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgdd.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgdd.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgdd.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgdd.spec

#---------------------------------------------#
# pg_tiktoken [RUST]
#---------------------------------------------#
pg_tiktoken:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_tiktoken*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_tiktoken.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_tiktoken.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_tiktoken.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_tiktoken.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_tiktoken.spec


###############################################################
#                         Obsolete                            #
###############################################################


#---------------------------------------------#
# pg_search [RUST]
#---------------------------------------------#
pg_search:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_search*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_search.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_search.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_search.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_search.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_search.spec

#---------------------------------------------#
# pg_lakehouse [RUST]
#---------------------------------------------#
pg_lakehouse:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_lakehouse*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_lakehouse.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_lakehouse.spec

#---------------------------------------------#
# pg_analytics [RUST] (Obsolete)
#---------------------------------------------#
pg_analytics:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_analytics*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_analytics.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_analytics.spec

#---------------------------------------------#
# pg_tier [RUST] (Obsolete)
#---------------------------------------------#
pg_tier:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_tier*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_tier.spec

#---------------------------------------------#
# libarrow-s3 (deps of parquet_s3_fdw)
#---------------------------------------------#
libarrow-s3:
	rm -rf ~/rpmbuild/RPMS/x86_64/libarrow-s3*.rpm;
	rpmbuild -ba ~/rpmbuild/SPECS/libarrow-s3.spec

#---------------------------------------------#
# parquet_s3_fdw (depend on parquet_s3_fdw)
#---------------------------------------------#
parquet_s3_fdw:
	rm -rf ~/rpmbuild/RPMS/x86_64/parquet_s3_fdw*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/parquet_s3_fdw.spec

#---------------------------------------------#
# unit (pg16 @ el8/el9) obsolete
#---------------------------------------------#
unit:
	./build unit 16

#---------------------------------------------#
# mysqlcompat (pg16 @ el8/el9)
#---------------------------------------------#
mysqlcompat:
	./build mysqlcompat 16

sslutils:
	./build sslutils 12 13 14 15 #16 17


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
	common zhparser duckdb_fdw pg_duckdb hunspell pg_roaringbitmap pgjwt pg_sqlog pg_hashids postgres_shacrypt permuteseq	vault supautils imgsmlr pg_similarity hydra age age15 pg_tde md5hash plv8 \
	rust pg_search pg_lakehouse pg_graphql pg_jsonschema wrappers pgmq pg_vectorize pg_later plprql pg_idkit pgsmcrypto pgvectorscale # pgdd pg_tiktoken pgml \
	debian preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pg_rrule pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo firebird_fdw \
	ls-rpm ls-srpm rm-rpm rm-srpm
