#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/rpm make shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2026-01-17
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   Apache-2.0
#==============================================================#
ARCH=$(shell uname -m)


###############################################################
#                            Prepare                          #
###############################################################
env: pig setup
pig:
	curl https://repo.pigsty.cc/pig | bash -s 0.7.0
setup: repo tool spec rust pgrx
repo:
	pig build repo
tool:
	pig build tool
spec:
	pig build spec
rust:
	pig build rust
pgrx: pgrx0161
pgrx0161:
	pig build pgrx -v 0.16.1


###############################################################
#                            Summary                          #
###############################################################
rust1: timescaledb_toolkit pg_polyline pg_tzf
rust2: vchord pg_summarize pg_tiktoken
rust3: pg_search vchord_bm25 pg_tokenizer pg_bestmatch
rust4: pglite_fusion pg_graphql pg_jsonschema wrappers
rust5: pg_parquet pg_render
rust6: plprql pg_smtp_client pg_idkit pgx_ulid
rust7: pg_base58 pg_convert pgdd pg_explain_ui
rust8: pg_session_jwt pg_anon pgsmcrypto pg_enigma
time: timescaledb pg_timeseries periods temporal_tables


###############################################################
#                       Category: TIME                        #
###############################################################
timescaledb:
	./build timescaledb 15 16 17

timescaledb_toolkit:	# rust pgrx 0.16.1
	./build timescaledb_toolkit 15 16 17 18

pg_timeseries:
	./build pg_timeseries 13 14 15 16 17 18

periods:
	./build periods 13 14 15 16 17 18

temporal_tables:
	./build temporal_tables 13 14 15 16 17 18

# emaj          (handled by PGDG)
# table_version (handled by PGDG)
# pg_cron       (handled by PGDG)
# pg_task       (handled by PGDG)

pg_later:       # rust 0.16.1
	./build pg_later 13 14 15 16 17

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

pg_polyline:    # rust pgrx 0.16.1
	./build pg_polyline 13 14 15 16 17 18

pg_tzf:         # rust pgrx 0.16.1
	./build pg_tzf 14 15 16 17 18


###############################################################
#                       Category: RAG                         #
###############################################################
pgvector:  # skip, handled by pgdg
	./build pgvector 13 14 15 16 17 18

vchord:    # rust pgrx 0.16.1
	./build vchord 13 14 15 16 17 18

pgvectorscale:  # rust 0.16.1
	./build pgvectorscale 14 15 16 17 18

pg_vectorize:	# rust 0.16.1
	./build pg_vectorize 14 15 16 17

pg_similarity:	# covered by pgdg
	./build pg_similarity 13 14 15 16 17 18

smlar:          # break for pg18, fixed
	./build smlar 13 14 15 16 17 18

pg_summarize:	# rust pgrx 0.16.1 (forked)
	./build pg_summarize 13 14 15 16 17

pg_tiktoken:	# rust pgrx 0.16.1
	./build pg_tiktoken 13 14 15 16 17 18

pg4ml:
	./build pg4ml 13 14 15 16 17 18

pgml:			# rust pgrx 0.12.9 (obsolete)
	./build pgml 14 15 16 17



###############################################################
#                       Category: FTS                         #
###############################################################
 pg_search:      # rust pgrx 0.16.1
	./build pg_search 15 16 17 18

pg_bigm:     	# covered by PGDG (deb break on 18)
	./build pg_bigm 13 14 15 16 17 18

pg_biscuit:
	./build pg_biscuit 16 17 18

pg_textsearch:
	./build pg_textsearch 17 18

pgroonga:
	./build pgroonga 13 14 15 16 17 18

# zhparser and scws deps
scws:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/scws*.rpm /tmp/pigsty-rpm/RPMS/scws*.rpm
	QA_RPATHS=2 rpmbuild -ba ~/rpmbuild/SPECS/scws.spec
scws-install:
	sudo yum remove -y scws || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/scws-1.2.3-1PIGSTY.el*.$(ARCH).rpm
zhparser:
	QA_RPATHS=2 ./build zhparser 13 14 15 16 17 18

pg_bestmatch:		# rust pgrx 0.16.1
	./build pg_bestmatch 13 14 15 16 17

vchord_bm25:		# rust  pgrx 0.16.1
	./build vchord_bm25 13 14 15 16 17 18

pg_tokenizer:		# rust pgrx 0.16.1
	./build pg_tokenizer 13 14 15 16 17 18

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
	./build citus 15 16 17

hydra:
	./build hydra 13 14 15 16 #17 not ready yet

#pg_analytics:   # download, obsolete
pg_duckdb:
	./build pg_duckdb 14 15 16 17 18

pg_mooncake:
	./build pg_mooncake 14 15 16 17 18

pg_clickhouse:
	./build pg_clickhouse 13 14 15 16 17 18

#duckdb_fdw:
#	./build duckdb_fdw

pg_parquet:			# rust pgrx 0.16.1 (manually bump from 0.16.0)
	./build pg_parquet 14 15 16 17 18

# pg_fkpart
pg_partman:
	./build pg_partman 14 15 16 17 18

# plproxy
# pg_strom

###############################################################
#                       Category: FEAT                        #
###############################################################
age:
	./build age 14 15 16 17 18

#hll:
#rum
pg_ai_query:
	./build pg_ai_query 14 15 16 17 18

pg_graphql:		# rust pgrx 0.16.1 (build on unpublished-release)
	./build pg_graphql 14 15 16 17 18

pg_jsonschema:	# rust pgrx 0.16.1 (patch from 0.16.0)
	./build pg_jsonschema 13 14 15 16 17 18

pg_ttl_index:
	./build pg_ttl_index 15 16 17 18

#jsquery:
#pg_hint_plan
index_advisor:
	./build index_advisor 13 14 15 16 17 18

pg_plan_filter:
	./build pg_plan_filter 13 14 15 16 17 18

imgsmlr:
	./build imgsmlr 13 14 15 16 17 18

#pg_ivm
pg_incremental:
	./build pg_incremental 16 17 18

pgmq:
	./build pgmq 13 14 15 16 17 18

# pgq
# orioledb

pg_cardano:
	./build pg_cardano 13 14 15 16 17 18

# rdkit
# omnigres

###############################################################
#                       Category: LANG                        #
###############################################################
pg_tle:
	./build pg_tle 13 14 15 16 17 18

plv8:
	./build plv8 13 14 15 16 17 18

pljs:
	./build pljs 14 15 16 17 18

# pllua

plprql: 		# rust pgrx 0.16.1
	./build plprql 13 14 15 16 17 18

# plprofiler
# plsh
# pljava
# plr
# pgtap
# faker
# db2


###############################################################
#                       Category: TYPE                        #
###############################################################
pg_prefix:
	./build pg_prefix 13 14 15 16 17 18

pg_semver:
	./build pg_semver 13 14 15 16 17 18

#unit:
pgpdf: 		# covered by PGDG
	./build pgpdf 13 14 15 16 17 18

pglite_fusion:
	./build pglite_fusion 13 14 15 16 17 18

md5hash:
	./build md5hash 13 14 15 16 17 18

asn1oid:
	./build asn1oid 13 14 15 16 17 18

pg_roaringbitmap:
	./build pg_roaringbitmap 13 14 15 16 17 18

pgfaceting:
	./build pgfaceting 13 14 15 16 17 18

pgsphere:
	./build pgsphere 13 14 15 16 17 18

pg_country:
	./build pg_country 13 14 15 16 17 18

pg_xenophile:
	./build pg_xenophile 13 14 15 16 17 18

pg_currency:
	./build pg_currency 13 14 15 16 17 18

pgcollection:
	./build pgcollection 14 15 16 17 18

numeral:
	./build numeral 13 14 15 16 17 18

pg_rational:
	./build pg_rational 13 14 15 16 17 18

pguint:
	./build pguint 13 14 15 16 17 18

pg_uint128:
	./build pg_uint128 13 14 15 16 17 18

hashtypes:
	./build hashtypes 13 14 15 16 17 18

pg_duration:
	./build pg_duration 17 18

pg_uri:
	./build pg_uri 13 14 15 16 17 18

pg_emailaddr:
	./build pg_emailaddr 13 14 15 16 17 18

pg_acl:
	./build pg_acl 13 14 15 16 17 18

pg_rrule:
	./build pg_rrule 13 14 15 16 17 18

chkpass:
	./build chkpass 13 14 15 16 17 18

#debversion:
#timestamp9:


###############################################################
#                       Category: UTIL                        #
###############################################################
pg_retry:
	./build pg_retry 17 18

pg_gzip:
	./build pg_gzip 13 14 15 16 17 18

pg_bzip:
	./build pg_bzip 13 14 15 16 17 18

pg_zstd:
	./build pg_zstd 13 14 15 16 17 18

pg_http:
	./build pg_http 13 14 15 16 17 18

pg_net:
	./build pg_net 13 14 15 16 17 18
pg_net2:
	./build pg_net2 13 14 15 16 17 18

pg_curl:
	./build pg_curl 13 14 15 16 17 18

pgjq:
	./build pgjq 14 15 16 17

pgjwt:
	./build pgjwt 13 14 15 16 17 18

pg_smtp_client:		# rust pgrx
	./build pg_smtp_client 14 15 16 17

pg_html5_email_address:
	./build pg_html5_email_address 13 14 15 16 17 18

url_encode:
	./build url_encode 13 14 15 16 17 18

#pgsql_tweaks (TODO)
#pg_extra_time

pgpcre:
	./build pgpcre 13 14 15 16 17 18

icu_ext:
	./build icu_ext 13 14 15 16 17 18

pgqr:
	./build pgqr 13 14 15 16 17 18

pg_protobuf:
	./build pg_protobuf 13 14 15 16 17 18

pg_envvar:
	./build pg_envvar 13 14 15 16 17 18

pg_render:		# rust pgrx 0.16.1
	./build pg_render 14 15 16 17

#pg_readme

ddl_historization:
	./build ddl_historization 13 14 15 16 17 18

data_historization:
	./build data_historization 13 14 15 16 17 18

pg_schedoc:
	./build pg_schedoc 13 14 15 16 17 18

pg_hashlib:
	./build pg_hashlib 13 14 15 16 17 18

pg_xxhash:
	./build pg_xxhash 13 14 15 16 17 18

shacrypt:
	./build shacrypt 13 14 15 16 17 18

cryptint:
	./build cryptint 13 14 15 16 17 18

pg_ecdsa:
	./build pg_ecdsa 13 14 15 16 17 18

pgsparql:
	./build pgsparql 13 14 15 16 17 18


###############################################################
#                       Category: FUNC                        #
###############################################################
pg_weighted_statistics:
	./build pg_weighted_statistics 13 14 15 16 17 18

pg_idkit:			# rust pgrx 0.16.1 (bump from 0.16.0)
	./build pg_idkit 13 14 15 16 17 18

pgx_ulid:			# rust pgrx 0.16.1
	./build pgx_ulid  14 15 16 17 18

#pg_uuidv7

permuteseq:
	./build permuteseq 13 14 15 16 17 18

pg_hashids:
	./build pg_hashids 13 14 15 16 17 18

sequential_uuids:
	./build sequential_uuids 13 14 15 16 17 18

pg_typeid:
	./build pg_typeid 13 14 15 16 17 18

quantile:
	./build quantile 13 14 15 16 17 18

lower_quantile:
	./build lower_quantile 13 14 15 16 17 18

count_distinct:
	./build count_distinct 13 14 15 16 17 18

omnisketch:
	./build omnisketch 13 14 15 16 17 18

ddsketch:
	./build ddsketch 13 14 15 16 17 18

vasco:
	./build vasco 13 14 15 16 17 18
	./build vasco 13 14 15 16 17 18

pgxicor:
	./build pgxicor 13 14 15 16 17 18

#tdigest

first_last_agg:
	./build first_last_agg 13 14 15 16 17 18

#extra_window_functions

floatvec:
	./build floatvec 13 14 15 16 17 18

aggs_for_vecs:
	./build aggs_for_vecs 13 14 15 16 17 18

aggs_for_arrays:
	./build aggs_for_arrays 13 14 15 16 17 18

pg_arraymath:
	./build pg_arraymath 13 14 15 16 17 18

pg_math:
	./build pg_math 13 14 15 16 17 18

pg_random:
	./build pg_random 13 14 15 16 17 18

pg_base36:
	./build pg_base36 13 14 15 16 17 18

pg_base62:
	./build pg_base62 13 14 15 16 17 18

pg_base58:		# rust (pgrx 0.16.1)
	./build pg_base58 13 14 15 16 17 18

pg_financial:
	./build pg_financial 13 14 15 16 17 18

pg_convert:		# rust (pgrx 0.16.1)
	./build pg_convert 14 15 16 17 18


###############################################################
#                       Category: ADMIN                       #
###############################################################
# pg_repack:
# pg_rewrite:
# pg_squeeze:
# pg_dirtyread:
# pg_prioritize:
# pg_checksums:
# pg_readonly:
# pg_permissions:
# pgautofailover:
# pg_catcheck:
# safeupdate:
# pgagent:
# pg_prewarm:
# pgpool:

pg_cooldown:
	./build pg_cooldown 13 14 15 16 17 18

ddlx:			# fix pgdg 18 missing
	./build ddlx 13 14 15 16 17 18

pglinter:
	./build pglinter 13 14 15 16 17 18

pgfincore:
	./build pgfincore 13 14 15 16 17 18

pgdd:			# rust pgrx 0.16.1
	./build pgdd 14 15 16 17 18

preprepare:
	./build preprepare 13 14 15 16 17 18

pg_upless:
	./build pg_upless 13 14 15 16 17 18

pgcozy:
	./build pgcozy 13 14 15 16 17 18

pg_orphaned:
	./build pg_orphaned 13 14 15 16 17 18

pg_crash:
	./build pg_crash 13 14 15 16 17 18

pg_cheat_funcs:
	./build pg_cheat_funcs 13 14 15 16 17 18

pg_fio:
	./build pg_fio 13 14 15 16 17 18

pg_savior:		# breaks on pg18 (fixed)
	./build pg_savior 13 14 15 16 17 18

pg_drop_events:
	./build pg_drop_events 13 14 15 16 17 18

table_log:
	./build table_log 13 14 15 16 17 18

###############################################################
#                       Category: STAT                         #
###############################################################
#pg_profile
#pg_show_plans
#pg_stat_kcache
#pg_stat_monitor      	# break on pg18
#pg_qualstats
#pg_track_settings
#pg_wait_sampling
#system_stats
#bgw_replstatus
#powa

pg_tracing:
	./build pg_tracing 14 15 16 17 18

pgsentinel:
	./build pgsentinel 13 14 15 16 17 18

pg_meta:
	./build pg_meta 13 14 15 16 17 18

pgnodemx:
	./build pgnodemx 13 14 15 16 17 18

pg_sqlog:
	./build pg_sqlog 13 14 15 16 17 18

pgmeminfo:
	./build pgmeminfo 13 14 15 16 17 18

toastinfo:
	./build toastinfo 13 14 15 16 17 18

pg_explain_ui:		# rust pgrx 0.16.1
	./build pg_explain_ui 13 14 15 16 17 18

pg_stat_monitor:
	./build pg_stat_monitor 18 # fix the missing pgdg

pg_store_plans:			# breaks on older version
	./build pg_store_plans 17 18 #14 15 16

pg_relusage:
	./build pg_relusage 13 14 15 16 17 18

pagevis:
	./build pagevis 13 14 15 16 17 18


###############################################################
#                       Category: SEC                         #
###############################################################
#passwordcheck_cracklib

#pg_tde
#pgaudit
#pgauditlogtofile
#pg_auth_mon
#credcheck
#pg_jobmon
#logerrors
#set_user

login_hook:
	./build login_hook 13 14 15 16 17 18

pg_noset:
	./build pg_noset 13 14 15 16 17 18

pg_vault:
	./build pg_vault 13 14 15 16 17 18

supautils:
	./build supautils 13 14 15 16 17 18

pgsodium:
	./build pgsodium 13 14 15 16 17 18

pg_session_jwt:		# rust pgrx 0.16.1
	./build pg_session_jwt 14 15 16 17 18

pg_anon:			# rust pgrx 0.16.1 (update from 0.16.0)
	./build pg_anon 13 14 15 16 17 18

pgsmcrypto:			# rust pgrx 0.16.1
	./build pgsmcrypto 13 14 15 16 17 18

pg_enigma:			# rust pgrx 0.16.1
	./build pgsmcrypto 14 15 16 17 18

pgcryptokey:
	./build pgcryptokey 13 14 15 16 17 18

pg_snakeoil:
	./build pg_snakeoil 13 14 15 16 17 18

pgextwlist:
	./build pgextwlist 13 14 15 16 17 18

pg_auditor:
	./build pg_auditor 13 14 15 16 17 18

sslutils:
	./build sslutils 13 14 15 16 17 18

###############################################################
#                       Category: FDW                         #
###############################################################
#multicorn
#odbc_fdw
#jdbc_fdw
#pgspider_ext
#mysql_fdw
#oracle_fdw
#tds_fdw
#db2_fdw
#pgbouncer_fdw
#mongo_fdw
#hdfs_fdw

wrappers:			# rust pgrx 0.16.1 (manual update from 0.16.0)
	./build wrappers 14 15 16 17 18

sqlite_fdw:
	./build sqlite_fdw 13 14 15 16 17 18

redis_fdw:
	./build redis_fdw 13 14 15 16 17 18

pg_redis_pubsub:
	./build pg_redis_pubsub 13 14 15 16 17 18

etcd_fdw:
	./build etcd_fdw 13 14 15 16 17 18

kafka_fdw:
	./build kafka_fdw 13 14 15 16 17

firebird_fdw:
	./build firebird_fdw 13 14 15 16 17 18

aws_s3:
	./build aws_s3 13 14 15 16 17 18

###############################################################
#                       Category: SIM                         #
###############################################################
#orafce
#pgtt
#pg_statement_rollback
#pg_dbms_metadata
#pg_dbms_lock
#pg_dbms_job
##babelfishpg
#pgmemcache

documentdb:
	./build documentdb 15 16 17 18

session_variable:
	./build session_variable 13 14 15 16 17 18

spat:
	./build spat 17

###############################################################
#                       Category: ETL                         #
###############################################################
#pglogical
#pgl_ddl_deploy
#wal2json
#wal2mongo
#decoderbufs
#repmgr
#pg_fact_loader

pglogical_ticker:
	./build pglogical_ticker 13 14 15 16 17 #18

pg_failover_slots:
	./build pg_failover_slots 13 14 15 16 17 18

db_migrator:
	./build db_migrator 13 14 15 16 17 18

libpgfeutils:	# require perl-FindBin
	./build libpgfeutils14 14
	./build libpgfeutils15 15
	./build libpgfeutils16 16
	./build libpgfeutils17 17
	./build libpgfeutils18 18

libpgfeutils-install:
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/libpgfeutils*$(ARCH).rpm

pgactive:
	./build pgactive 13 14 15 16 17 18

decoder_raw:
	./build decoder_raw 13 14 15 16 17 18

mimeo:
	./build mimeo 13 14 15 16 17 18

pg_bulkload:
	./build pg_bulkload 13 14 15 16 17 18


###############################################################
#                          Misc                               #
###############################################################
pg_filedump:
	./build pg_filedump 18

###############################################################
#                       Kernels                               #
###############################################################
openhalodb:
	rpmbuild -ba SPECS/openhalodb.spec
oriolepg:
	rpmbuild -ba SPECS/oriolepg_17.spec
oriolepg-install:
	sudo yum remove -y oriolepg_17 || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/oriolepg_17*.$(ARCH).rpm
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
#                      .PHONY Targets                         #
###############################################################
# All targets declared as .PHONY to ensure make always runs them
# even if a file with the same name exists

.PHONY: default env pig setup repo tool spec rust pgrx pgrx0161 pgrx0129

.PHONY: deps scws scws-install libduckdb libduckdb-install \
	libpgfeutils libpgfeutils-install pg_filedump

.PHONY: age aggs_for_arrays aggs_for_vecs asn1oid aws_s3 \
	chkpass citus count_distinct cryptint \
	data_historization db_migrator ddl_historization ddlx pglinter ddsketch \
	decoder_raw documentdb firebird_fdw first_last_agg floatvec \
	geoip hashtypes hunspell hunspell_cs_cz hunspell_de_de \
	hunspell_en_us hunspell_fr hunspell_ne_np hunspell_nl_nl \
	hunspell_nn_no hunspell_pt_pt hunspell_ru_ru hunspell_ru_ru_aot \
	hydra icu_ext imgsmlr pg_ttl_index index_advisor etcd_fdw kafka_fdw \
	lower_quantile md5hash mimeo numeral omnisketch \
	openhalodb orioledb oriolepg oriolepg-install pagevis \
	periods permuteseq pg_acl pg_anon pg_arraymath pg_auditor \
	pg_base36 pg_base58 pg_base62 pg_bestmatch pg_bigm pg_biscuit pg_textsearch pg_bulkload \
	pg_bzip pg_cardano pg_cheat_funcs pg_convert pg_cooldown \
	pg_country pg_crash pg_curl pg_currency pg_drop_events \
	pg_duckdb pg_duration pg_ecdsa pg_emailaddr pg_envvar \
	pg_explain_ui pg_failover_slots pg_financial pg_fio \
	pg_geohash pg_ai_query pg_graphql pg_gzip pg_hashids pg_hashlib \
	pg_html5_email_address pg_http pg_idkit pg_incremental \
	pg_jsonschema pg_later pg_math pg_meta pg_mooncake pg_clickhouse \
	pg_net pg_net2 pg_noset pg_orphaned pg_parquet pg_plan_filter \
	pg_polyline pg_protobuf pg_random pg_rational pg_redis_pubsub \
	pg_relusage pg_render pg_retry pg_roaringbitmap pg_savior pg_schedoc \
	pg_semver pg_session_jwt pg_similarity pg_smtp_client \
	pg_snakeoil pg_sqlog pg_store_plans pg_summarize pg_tde \
	pg_tiktoken pg_timeseries pg_tle pg_tokenizer pg_tracing \
	pg_tzf pg_uint128 pg_upless pg_uri pg_vault pg_vectorize \
	pg_weighted_statistics pg_xenophile pg_xxhash pg_zstd pg4ml pgactive pgcollection \
	pgcozy pgcryptokey pgdd pgextwlist pgfaceting pgjq pgjwt \
	pglite_fusion pgmeminfo pgml pgmq pgnodemx pgpcre pgpdf \
	pgqr pgroonga pgsentinel pgsmcrypto pg_enigma pgsodium pgsparql \
	pgsphere pguint pgvector pgvectorscale pgx_ulid pgxicor \
	pg_partman pljs plproxy plprql plv8 prefix preprepare q3c quantile \
	redis_fdw sequential_uuids pg_typeid session_variable shacrypt \
	smlar spat sqlite_fdw sslutils supautils table_log \
	temporal_tables timescaledb timescaledb_toolkit toastinfo \
	url_encode vasco vchord vchord_bm25 wrappers zhparser \
	pglogical_ticker omnigres \
	ls-rpm ls-srpm rm-rpm rm-srpm rmdbg


