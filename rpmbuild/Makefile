#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2025-06-24
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   AGPLv3
#==============================================================#
ARCH=$(shell uname -m)




###############################################################
#                       Category: TIME                        #
###############################################################
timescaledb:
	./build timescaledb nodebug 15 16 17

pg_timeseries:
	./build pg_timeseries nodebug 13 14 15 16 17 18

periods:
	./build periods nodebug 13 14 15 16 17 18

temporal_tables:
	./build temporal_tables 13 14 15 16 17 18

# emaj          (handled by PGDG)
# table_version (handled by PGDG)
# pg_cron       (handled by PGDG)
# pg_task       (handled by PGDG)

pg_later:       # rust 0.12.5 (TBD for 18)
	./build pg_later nodebug 13 14 15 16 17

# pg_background (handled by PGDG)


###############################################################
#                       Category: GIS                         #
###############################################################

# postgis
# pgroutine
# pointcloud
# h3 (missing el8 17/18)
# ogr_fdw

q3c:
	./build q3c 13 14 15 16 17 18

geoip:
	./build geoip 13 14 15 16 17 18

pg_geohash:
	./build pg_geohash 13 14 15 16 17 18

pg_polyline:    # rust (TBD for 18)
	./build pg_polyline nodebug 13 14 15 16 17

pg_tzf:         # rust pgrx 0.16.1
	./build pg_tzf nodebug 14 15 16 17 18


###############################################################
#                       Category: RAG                         #
###############################################################
pgvector:  # skip, handled by pgdg
	./build pgvector nodebug 13 14 15 16 17 18

vchord:    # rust pgrx 0.16.1
	./build vchord nodebug 13 14 15 16 17 18

pgvectorscale:  # rust 0.12.9 TBD for pg18
	./build pgvectorscale nodebug 13 14 15 16 17

pg_vectorize:	# rust 0.25.0 pgrx 0.13.1
	./build pg_vectorize nodebug 14 15 16 17

pg_similarity:	# covered by pgdg
	./build pg_similarity 13 14 15 16 17 18

smlar:          # break for pg18
	./build smlar 13 14 15 16 17

pg_summarize:	# rust pgrx 0.16.1 (forked)
	./build pg_summarize nodebug 13 14 15 16 17

pg_tiktoken:	# rust pgrx 0.16.1
	./build pg_tiktoken nodebug 13 14 15 16 17 18

pg4ml:
	./build pg4ml 13 14 15 16 17 18

pgml:			# rust pgrx 0.12.9 (obsolete)
	./build pgml nodebug 14 15 16 17



###############################################################
#                       Category: FTS                         #
###############################################################
# pg_search     # download directly
pg_bigm:     	# covered by PGDG (deb break on 18)
	./build pg_bigm nodebug 13 14 15 16 17 18

# pgroonga: TBD

# zhparser and scws deps
scws:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/scws*.rpm /tmp/pigsty-rpm/RPMS/scws*.rpm
	QA_RPATHS=2 rpmbuild -ba ~/rpmbuild/SPECS/scws.spec
scws-install:
	sudo yum remove -y scws || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/scws-1.2.3-1PIGSTY.el*.$(ARCH).rpm
zhparser:
	QA_RPATHS=2 ./build zhparser 13 14 15 16 17 18

pg_bestmatch:		# rust pgrx 0.12.7 (obsolete)
	./build pg_bestmatch nodebug 13 14 15 16 17

vchord_bm25:		# rust  pgrx 0.16.1
	./build vchord_bm25 nodebug 13 14 15 16 17 18

pg_tokenizer:		# rust pgrx 0.16.1
	./build pg_tokenizer nodebug 13 14 15 16 17 18

hunspell: hunspell_cs_cz hunspell_de_de hunspell_en_us hunspell_fr hunspell_ne_np hunspell_nl_nl hunspell_nn_no hunspell_ru_ru hunspell_ru_ru_aot #hunspell_pt_pt
hunspell_cs_cz:
	./build hunspell_cs_cz     13 14 15 16 17 18
hunspell_de_de:
	./build hunspell_de_de     13 14 15 16 17 18
hunspell_en_us:
	./build hunspell_en_us     13 14 15 16 17 18
hunspell_fr:
	./build hunspell_fr        13 14 15 16 17 18
hunspell_ne_np:
	./build hunspell_ne_np     13 14 15 16 17 18
hunspell_nl_nl:
	./build hunspell_nl_nl     13 14 15 16 17 18
hunspell_nn_no:
	./build hunspell_nn_no     13 14 15 16 17 18
hunspell_ru_ru:
	./build hunspell_ru_ru     13 14 15 16 17 18
hunspell_ru_ru_aot:
	./build hunspell_ru_ru_aot 13 14 15 16 17 18
hunspell_pt_pt:
	./build hunspell_pt_pt     13 14 15 16 17 18

###############################################################
#                       Category: FTS                         #
###############################################################
citus:			# not ready for pg18
	./build citus nodebug 15 16 17

hydra:
	./build hydra 13 14 15 16 #17 not ready yet

#pg_analytics:   # download, obsolete
pg_duckdb:
	./build pg_duckdb 14 15 16 17 18

pg_mooncake:
	./build pg_mooncake 14 15 16 17

#duckdb_fdw

pg_parquet:			# rust pgrx 0.16.1 (manually bump from 0.16.0)
	./build pg_parquet 14 15 16 17 18

# pg_fkpart
# pg_partman
# plproxy
# pg_strom

###############################################################
#                       Category: FEAT                        #
###############################################################
age:
	./build age 14 15 16 17

#hll:
#rum
pg_graphql:		# rust pgrx 0.16.1 (build on unpublished-release)
	./build pg_graphql nodebug 14 15 16 17 18

pg_jsonschema:	# rust pgrx 0.16.1 (patch from 0.16.0)
	./build pg_jsonschema nodebug 13 14 15 16 17 18

#jsquery:
#pg_hint_plan
index_advisor:
	./build index_advisor

pg_plan_filter:
	./build pg_plan_filter

imgsmlr:
	./build imgsmlr

#pg_ivm
pg_incremental:
	./build pg_incremental 16 17

pgmq:
	./build pgmq nodebug

# pgq
# orioledb
# pg_cardano
# rdkit
# omnigres

###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################
###############################################################
#                       Category: FTS                         #
###############################################################













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



# depend on libduckdb
duckdb_fdw:
	./build duckdb_fdw






pg_tde:
	./build pg_tde 16

# supabase extensions
pgjwt:
	./build pgjwt nodebug

vault:
	./build vault

supautils:
	./build supautils 13 14 15 16 17



plv8:
	./build plv8

omnigres:
	./build omnigres


pgroonga:
	./build pgroonga 13 14 15 16 17



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





md5hash:
	./build md5hash

preprepare:
	./build preprepare

first_last_agg:
	./build first_last_agg

pgpcre:
	./build pgpcre

icu_ext:
	./build icu_ext 13 14 15 16 17 18

asn1oid:
	./build asn1oid 13 14 15 16 17 18

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
	./build toastinfo 13 14 15 16 17 18



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
	./build pg_envvar nodebug
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

plproxy:
	./build plproxy   # el8/el9
table_version:
	./build table_version   # el8/el9
ddlx:
	./build ddlx 13 14 15 16 17 18
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

acl:
	./build acl
pg_emailaddr:
	./build pg_emailaddr



pg_uint128:
	./build pg_uint128 13 14 15 16 17 18
pg_relusage:
	./build pg_relusage
pg_net:
	./build pg_net

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
	./build pg_tracing 14 15 16 17
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
pg_tle:
	./build pg_tle


# not included
logfmt:
	./build logfmt 15 16
pg_kaboom:
	./build pg_kaboom 13 14 15 16
jsonb_apply:
	./build jsonb_apply
sqlite_fdw:
	./build sqlite_fdw
pgsentinel:
	./build pgsentinel
spat:
	./build spat 17
libpgfeutils:
	./build libpgfeutils14 14
	./build libpgfeutils15 15
	./build libpgfeutils16 16
	./build libpgfeutils17 17
	./build libpgfeutils18 18
libpgfeutils-install:
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/libpgfeutils*$(ARCH).rpm
pgactive:
	./build pgactive
pg_rewrite:
	./build pg_rewrite

###############################################################
#               6. RUST / PGRX Extensions                     #
###############################################################
rust1: pg_graphql pg_jsonschema wrappers pg_idkit pgsmcrypto pg_tiktoken pg_summarize pg_polyline pg_explain_ui pg_cardano pg_base58 pg_parquet pg_vectorize pgvectorscale vchord pglite_fusion pg_bestmatch pg_later pg_smtp_client timescaledb_toolkit pgdd pg_tokenizer
rust2: pgml plprql
rusta: pg_graphql pg_jsonschema wrappers pg_idkit pg_later
rustb: pgsmcrypto pg_tiktoken pg_summarize pg_polyline pg_explain_ui
rustc: pg_cardano pg_base58 pg_parquet pg_vectorize pgvectorscale
rustd: vchord pglite_fusion pg_bestmatch pg_session_jwt pg_smtp_client

# pgrx 0.12.9

wrappers:
	./build wrappers nodebug 14 15 16 17
pg_idkit:
	./build pg_idkit nodebug

pg_anon:
	./build pg_anon nodebug 13 14 15 16 17
timescaledb_toolkit:
	./build timescaledb_toolkit nodebug 15 16 17

pgsmcrypto:
	./build pgsmcrypto nodebug



pg_explain_ui:
	./build pg_explain_ui nodebug
pg_cardano:
	./build pg_cardano nodebug
pg_base58:
	./build pg_base58 nodebug
pg_parquet:
	./build pg_parquet nodebug 14 15 16 17


pg_session_jwt:
	./build pg_session_jwt nodebug 14 15 16 17
pglite_fusion:
	./build pglite_fusion nodebug

pg_smtp_client:
	./build pg_smtp_client nodebug 14 15 16 17



pg_render:
	./build pg_render nodebug 14 15 16 17
convert:
	./build convert nodebug 13 14 15 16 17
pgdd:
	./build pgdd nodebug
pgx_ulid:
	./build pgx_ulid nodebug


# pgrx 0.11.4
plprql:
	./build plprql nodebug 12 13 14 15 16



###############################################################
#                       Kernels                               #
###############################################################
openhalodb:
	rpmbuild -ba SPECS/openhalodb.spec
oriolepg:
	rpmbuild -ba SPECS/oriolepg_17.spec
orioledb:
	rpmbuild -ba SPECS/orioledb_17.spec

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

rmdbg:
	mkdir -p RPMS/el8.x86_64/tmp RPMS/el9.x86_64/tmp RPMS/el8.aarch64/tmp RPMS/el9.aarch64/tmp
	mv RPMS/el8.x86_64/*debug* RPMS/el8.x86_64/tmp/
	mv RPMS/el8.aarch64/*debug* RPMS/el8.aarch64/tmp/
	mv RPMS/el9.x86_64/*debug* RPMS/el9.x86_64/tmp/
	mv RPMS/el9.aarch64/*debug* RPMS/el9.aarch64/tmp/



###############################################################
#                      Inventory                              #
###############################################################
.PHONY: default deps scws scws-install libduckdb libduckdb-install \
	deps scws scws-install libduckdb libduckdb-install pg_filedump \
	batch1 zhparser duckdb_fdw hunspell hydra age pg_tde pgjwt vault supautils index_advisor plv8 pg_duckdb pgroonga timescaledb citus omnigres pg_mooncake \
	batch2 pg_roaringbitmap pg_sqlog pg_hashids postgres_shacrypt permuteseq imgsmlr pg_similarity md5hash preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo \
	batch3 pg_orphaned pgcozy decoder_raw pg_failover_slots pg_financial pg_savior aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address quantile lower_quantile pg_timeit pg_random session_variable chkpass pg_currency pg_uri cryptint floatvec pg_auditor noset redis_fdw \
	aggs_for_arrays pg_meta pg_redis_pubsub pg_arraymath pagevis pg_ecdsa pg_cheat_funcs pg_crash pg_math firebird_fdw sequential_uuids pgnodemx pg_hashlib pg_protobuf pg_country pg_fio aws_s3 \
	batch4 geoip plproxy table_version kafka_fdw log_fdw pgqr pg_zstd pg_geohash acl pg_emailaddr smlar pgmq pg_timeseries pg_plan_filter pg_relusage pg_uint128 pg4ml pgpdf pgsodium \
	omnisketch ddsketch pg_duration ddl_historization data_historization pg_schedoc floatfile pg_upless vasco pg_xxhash pg_xenophile pg_drop_events documentdb pg_tracing pg_curl pgxicor pgsparql pgjq hashtypes db_migrator pg_bulkload pg_cooldown pg_mustach \
	sqlite_fdw jsonb_apply pgsentinel spat libpgfeutils libpgfeutils-install pgactive pgcollection pg_bzip pg_tle pg_incremental \
	rust rust1 rust2 rust3 rusta rustb rustc rustd \
	pg_graphql pg_jsonschema wrappers pg_idkit pgsmcrypto pg_tiktoken pg_summarize pg_tzf pg_polyline pg_explain_ui pg_cardano pg_base58 pg_parquet pg_vectorize timescaledb_toolkit pgvectorscale vchord vchord_bm25 pg_tokenizer pg_render convert \
	pglite_fusion pg_bestmatch pgml plprql pg_later pg_smtp_client pgdd pgx_ulid \
	openhalodb oriolepg orioledb \
	ls-rpm ls-srpm rm-rpm rm-srpm


