#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2025-10-27
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   Apache-2.0
#==============================================================#
ARCH=$(shell uname -m)


###############################################################
#                       Category: TIME                        #
###############################################################
timescaledb:
	./build timescaledb nodebug 15 16 17

timescaledb_toolkit:
	./build timescaledb nodebug 15 16 17 18

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

pg_polyline:    # rust pgrx 0.16.1
	./build pg_polyline nodebug 13 14 15 16 17 18

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

#duckdb_fdw:
#	./build duckdb_fdw

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
	./build index_advisor 13 14 15 16 17 18

pg_plan_filter:
	./build pg_plan_filter 13 14 15 16 17 18

imgsmlr:
	./build imgsmlr 13 14 15 16 17 18

#pg_ivm
pg_incremental:
	./build pg_incremental 16 17 18

pgmq:
	./build pgmq nodebug 13 14 15 16 17 18

# pgq
# orioledb

pg_cardano:
	./build pg_cardano nodebug 13 14 15 16 17 18

# rdkit
# omnigres

###############################################################
#                       Category: LANG                        #
###############################################################
pg_tle:
	./build pg_tle 13 14 15 16 17 18

plv8:
	./build plv8 13 14 15 16 17 18

# pllua

plprql: 		# rust pgrx 0.11.4
	./build plprql nodebug 13 14 15 16

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
prefix:
	./build prefix nodebug 13 14 15 16 17 18

pg_semver:
	./build pg_semver nodebug 13 14 15 16 17 18

#unit:
pgpdf: 		# covered by PGDG
	./build pgpdf nodebug 13 14 15 16 17 18

pglite_fusion:
	./build pglite_fusion nodebug 13 14 15 16 17 18

md5hash:
	./build md5hash nodebug 13 14 15 16 17 18

asn1oid:
	./build asn1oid nodebug 13 14 15 16 17 18

pg_roaringbitmap:
	./build pg_roaringbitmap nodebug 13 14 15 16 17 18

pgfaceting:
	./build pgfaceting nodebug 13 14 15 16 17 18

pgsphere:
	./build pgsphere nodebug 13 14 15 16 17 18

pgsphere:
	./build pgsphere nodebug 13 14 15 16 17 18

pg_country:
	./build pg_country nodebug 13 14 15 16 17 18

pg_xenophile:
	./build pg_xenophile nodebug 13 14 15 16 17 18

pg_currency:
	./build pg_currency nodebug 13 14 15 16 17 18

pgcollection:
	./build pgcollection nodebug 14 15 16 17 18

numeral:
	./build numeral nodebug 13 14 15 16 17 18

pg_rational:
	./build pg_rational nodebug 13 14 15 16 17 18

pguint:
	./build pguint nodebug 13 14 15 16 17 18

pg_uint128:
	./build pg_uint128 nodebug 13 14 15 16 17 18

hashtypes:
	./build hashtypes nodebug 13 14 15 16 17 18

pg_duration:
	./build pg_duration 17 18

pg_uri:
	./build pg_uri nodebug 13 14 15 16 17 18

pg_emailaddr:
	./build pg_emailaddr nodebug 13 14 15 16 17 18

pg_acl:
	./build pg_acl nodebug 13 14 15 16 17 18

#debversion:
#pg_rrule:
#timestamp9:

chkpass:
	./build chkpass nodebug 13 14 15 16 17 18




###############################################################
#                       Category: UTIL                        #
###############################################################
pg_gzip:
	./build pg_gzip nodebug 13 14 15 16 17 18

pg_bzip:
	./build pg_bzip nodebug 13 14 15 16 17 18

pg_zstd:
	./build pg_zstd nodebug 13 14 15 16 17 18

pg_http:
	./build pg_http nodebug 13 14 15 16 17 18

pg_net:
	./build pg_net nodebug 13 14 15 16 17 18
pg_net2:
	./build pg_net2 nodebug 13 14 15 16 17 18

pg_curl:
	./build pg_curl nodebug 13 14 15 16 17 18

pgjq:
	./build pgjq nodebug 14 15 16 17

pgjwt:
	./build pgjwt nodebug 13 14 15 16 17 18

pg_smtp_client:		# rust pgrx
	./build pg_smtp_client nodebug 14 15 16 17

pg_html5_email_address:
	./build pg_html5_email_address nodebug 13 14 15 16 17 18

url_encode:
	./build url_encode nodebug 13 14 15 16 17 18

#pgsql_tweaks (TODO)
#pg_extra_time

pgpcre:
	./build pgpcre nodebug 13 14 15 16 17 18

icu_ext:
	./build icu_ext nodebug 13 14 15 16 17 18

pgqr:
	./build pgqr nodebug 13 14 15 16 17 18

pg_protobuf:
	./build pg_protobuf nodebug 13 14 15 16 17 18

pg_envvar:
	./build pg_envvar nodebug 13 14 15 16 17 18

pg_render:		# rust
	./build pg_render nodebug 14 15 16 17

#pg_readme

ddl_historization:
	./build ddl_historization nodebug 13 14 15 16 17 18

data_historization:
	./build data_historization nodebug 13 14 15 16 17 18

pg_schedoc:
	./build pg_schedoc nodebug 13 14 15 16 17 18

pg_hashlib:
	./build pg_hashlib nodebug 13 14 15 16 17 18

pg_xxhash:
	./build pg_xxhash nodebug 13 14 15 16 17 18

shacrypt:
	./build shacrypt nodebug 13 14 15 16 17 18

cryptint:
	./build cryptint nodebug 13 14 15 16 17 18

pg_ecdsa:
	./build pg_ecdsa nodebug 13 14 15 16 17 18

pgsparql:
	./build pgsparql nodebug 13 14 15 16 17 18


###############################################################
#                       Category: FUNC                        #
###############################################################

pg_idkit:			# rust pgrx 0.16.1 (bump from 0.16.0)
	./build pg_idkit nodebug 13 14 15 16 17 18

pgx_ulid:			# rust pgrx 0.16.1
	./build pgx_ulid  nodebug 14 15 16 17 18

#pg_uuidv7

permuteseq:
	./build permuteseq nodebug 13 14 15 16 17 18

pg_hashids:
	./build pg_hashids nodebug 13 14 15 16 17 18

sequential_uuids:
	./build sequential_uuids nodebug 13 14 15 16 17 18

quantile:
	./build quantile nodebug 13 14 15 16 17 18

lower_quantile:
	./build lower_quantile nodebug 13 14 15 16 17 18

count_distinct:
	./build count_distinct nodebug 13 14 15 16 17 18

omnisketch:
	./build omnisketch nodebug 13 14 15 16 17 18

ddsketch:
	./build ddsketch nodebug 13 14 15 16 17 18

vasco:
	./build vasco nodebug 13 14 15 16 17 18
	./build vasco nodebug 13 14 15 16 17 18

pgxicor:
	./build pgxicor nodebug 13 14 15 16 17 18

#tdigest

first_last_agg:
	./build first_last_agg nodebug 13 14 15 16 17 18

#extra_window_functions

floatvec:
	./build floatvec nodebug 13 14 15 16 17 18

aggs_for_vecs:
	./build aggs_for_vecs nodebug 13 14 15 16 17 18

aggs_for_arrays:
	./build aggs_for_arrays nodebug 13 14 15 16 17 18

pg_arraymath:
	./build pg_arraymath nodebug 13 14 15 16 17 18

pg_math:
	./build pg_math nodebug 13 14 15 16 17 18

pg_random:
	./build pg_random nodebug 13 14 15 16 17 18

pg_base36:
	./build pg_base36 nodebug 13 14 15 16 17 18

pg_base62:
	./build pg_base62 nodebug 13 14 15 16 17 18

pg_base58:		# rust (pgrx 0.16.1)
	./build pg_base58 nodebug 13 14 15 16 17 18

pg_financial:
	./build pg_financial nodebug 13 14 15 16 17 18

pg_convert:		# rust (pgrx 0.16.1)
	./build pg_convert nodebug 13 14 15 16 17 18


###############################################################
#                       Category: ADMIN                       #
###############################################################
# pg_repack:
# pg_rewrite:
# pg_squeeze:
# pg_dirtyread:
# pgfincore:
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
	./build pg_cooldown nodebug 13 14 15 16 17 18

ddlx:			# fix pgdg 18 missing
	./build ddlx nodebug 13 14 15 16 17 18

pgdd:			# rust pgrx 0.16.1
	./build pgdd nodebug 13 14 15 16 17 18

preprepare:
	./build preprepare nodebug 13 14 15 16 17 18

pg_upless:
	./build pg_upless nodebug 13 14 15 16 17 18

pgcozy:
	./build pgcozy nodebug 13 14 15 16 17 18

pg_orphaned:
	./build pg_orphaned nodebug 13 14 15 16 17 18

pg_crash:
	./build pg_crash nodebug 13 14 15 16 17 18

pg_cheat_funcs:
	./build pg_cheat_funcs nodebug 13 14 15 16 17 18

pg_fio:
	./build pg_fio nodebug 13 14 15 16 17 18

pg_savior:		# breaks on pg18
	./build pg_savior nodebug 13 14 15 16 17

pg_drop_events:
	./build pg_drop_events nodebug 13 14 15 16 17 18

table_log:
	./build table_log nodebug 13 14 15 16 17 18

###############################################################
#                       Category: STAT                         #
###############################################################
#pg_profile
#pg_show_plans
#pg_stat_kcache
#pg_stat_monitor      	# break on pg18
#pg_qualstats
#pg_store_plans			# breaks on pg18
#pg_track_settings
#pg_wait_sampling
#system_stats
#bgw_replstatus
#powa

pg_tracing:
	./build pg_tracing nodebug 14 15 16 17 18

pgsentinel:
	./build pgsentinel nodebug 13 14 15 16 17 18

pg_meta:
	./build pg_meta nodebug 13 14 15 16 17 18

pgnodemx:
	./build pgnodemx nodebug 13 14 15 16 17 18

pg_sqlog:
	./build pg_sqlog nodebug 13 14 15 16 17 18

pgmeminfo:
	./build pgmeminfo nodebug 13 14 15 16 17 18

toastinfo:
	./build toastinfo nodebug 13 14 15 16 17 18

pg_explain_ui:		# rust pgrx 0.12.9
	./build pg_explain_ui nodebug 13 14 15 16 17 18

pg_relusage:
	./build pg_relusage nodebug 13 14 15 16 17 18

pagevis:
	./build pagevis nodebug 13 14 15 16 17 18


###############################################################
#                       Category: SEC                         #
###############################################################
#passwordcheck_cracklib
#pg_vault
#pg_tde
#pgaudit
#pgauditlogtofile
#pg_auth_mon
#credcheck
#pg_jobmon
#logerrors
#login_hook
#set_user
#pg_noset

supautils:
	./build supautils nodebug 13 14 15 16 17 18

pgsodium:
	./build pgsodium nodebug 13 14 15 16 17 18

pg_session_jwt:		# rust pgrx 0.16.1
	./build pg_session_jwt nodebug 14 15 16 17 18

pg_anon:			# rust pgrx 0.16.1 (update from 0.16.0)
	./build pg_anon nodebug 13 14 15 16 17 18

pgsmcrypto:			# rust pgrx 0.16.1
	./build pgsmcrypto nodebug 13 14 15 16 17 18

pgcryptokey:
	./build pgcryptokey nodebug 13 14 15 16 17 18

pg_snakeoil:
	./build pg_snakeoil nodebug 13 14 15 16 17 18

pgextwlist:
	./build pgextwlist nodebug 13 14 15 16 17 18

pg_auditor:
	./build pg_auditor nodebug 13 14 15 16 17 18

sslutils:
	./build sslutils nodebug 13 14 15 16 17 18

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
	./build wrappers nodebug 14 15 16 17 18

sqlite_fdw:
	./build sqlite_fdw nodebug 13 14 15 16 17 18

redis_fdw:
	./build redis_fdw nodebug 13 14 15 16 17 18

pg_redis_pubsub:
	./build pg_redis_pubsub nodebug 13 14 15 16 17 18

kafka_fdw:
	./build kafka_fdw nodebug 13 14 15 16 17

firebird_fdw:
	./build firebird_fdw nodebug 13 14 15 16 17 18

aws_s3:
	./build aws_s3 nodebug 13 14 15 16 17 18

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
	./build documentdb nodebug 15 16 17

session_variable:
	./build session_variable nodebug 13 14 15 16 17 18

spat:
	./build spat nodebug 17

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
	./build pglogical_ticker nodebug 13 14 15 16 17 #18

pg_failover_slots:
	./build pg_failover_slots nodebug 13 14 15 16 17 18

db_migrator:
	./build db_migrator nodebug 13 14 15 16 17 18

libpgfeutils:	# require perl-FindBin
	./build libpgfeutils14 14
	./build libpgfeutils15 15
	./build libpgfeutils16 16
	./build libpgfeutils17 17
	./build libpgfeutils18 18

libpgfeutils-install:
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/libpgfeutils*$(ARCH).rpm

pgactive:
	./build pgactive nodebug 13 14 15 16 17 18

decoder_raw:
	./build decoder_raw nodebug 13 14 15 16 17 18

mimeo:
	./build mimeo nodebug 13 14 15 16 17 18

pg_bulkload:
	./build pg_bulkload nodebug 13 14 15 16 17 18






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


