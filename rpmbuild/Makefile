#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/rpm make shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2026-07-21
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   Apache-2.0
#==============================================================#
ARCH=$(shell uname -m)
PG_MAJOR ?= 18


###############################################################
#                            Prepare                          #
###############################################################
env: pig setup
pig:
	curl https://repo.pigsty.cc/pig | bash
setup: repo tool spec rust pgrx
repo:
	pig build repo
tool:
	pig build tool
spec:
	pig build spec
rust:
	pig build rust
pgrx: pgrx0191
pgrx0161:
	pig build pgrx -v 0.16.1
pgrx0170:
	pig build pgrx -v 0.17.0
pgrx0180:
	pig build pgrx -v 0.18.0
pgrx0181:
	pig build pgrx -v 0.18.1
pgrx0191:
	pig build pgrx -v 0.19.1

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
rust8: pg_session_jwt pg_oidc_validator_rust pg_anon pgsmcrypto pg_enigma
rust9: pg_pinyin pg_eviltransform
rust10: pg_command_fw pg_trickle pggraph pgrdf jsonschema
time: timescaledb timescaledb_toolkit pg_timeseries periods temporal_tables pg_task pg_later pg_background pg_when pg_stl cron_utils pg_extra_time pg_bikram_sambat


###############################################################
#                       Category: TIME                        #
###############################################################
timescaledb:
	./build timescaledb 15 16 17 18

timescaledb_toolkit:	# rust pgrx 0.19.1
	./build timescaledb_toolkit 15 16 17 18

pg_timeseries:
	./build pg_timeseries 14 15 16 17 18

periods:
	./build periods 14 15 16 17 18

temporal_tables:
	./build temporal_tables 14 15 16 17 18

# emaj          (handled by PGDG)
# table_version (handled by PGDG)
# pg_cron       (handled by PGDG)
pg_task:
	./build pg_task 14 15 16 17 18

pg_later:       # rust pgrx 0.19.1
	./build pg_later 14 15 16 17 18

pg_background:
	./build pg_background 14 15 16 17 18

pg_when:        # rust pgrx 0.19.1
	./build pg_when 14 15 16 17 18

pg_stl:
	./build pg_stl 16 17 18

cron_utils:
	./build cron_utils 14 15 16 17 18


###############################################################
#                       Category: GIS                         #
###############################################################

# postgis
# pgroutine
# pointcloud
h3-pg:         # EL8 x86_64 gap only
	./build h3-pg 17 18
# ogr_fdw

q3c:
	./build q3c 14 15 16 17 18

geoip:
	./build geoip 14 15 16 17 18

pg_polyline:    # rust pgrx 0.19.1
	./build pg_polyline 14 15 16 17 18

pg_eviltransform:	# rust pgrx 0.19.1
	./build pg_eviltransform 14 15 16 17 18

pg_geohash:
	./build pg_geohash 14 15 16 17 18

mobilitydb:
	./build mobilitydb 14 15 16 17 18

pghydro:
	./build pghydro 14 15 16 17 18

pg_tzf:         # rust pgrx 0.19.1
	./build pg_tzf 14 15 16 17 18


###############################################################
#                       Category: RAG                         #
###############################################################
pgvector:  # skip, handled by pgdg
	./build pgvector 14 15 16 17 18

vchord:    # rust pgrx 0.19.1
	./build vchord 14 15 16 17 18

pgvectorscale:  # rust pgrx 0.19.1
	./build pgvectorscale 14 15 16 17 18

pg_vectorize:	# rust pgrx 0.19.1
	./build pg_vectorize 14 15 16 17 18

pg_similarity:	# covered by pgdg
	./build pg_similarity 14 15 16 17 18

pg_rrf:			# rust pgrx 0.19.1
	./build pg_rrf 14 15 16 17 18

smlar:          # break for pg18, fixed
	./build smlar 14 15 16 17 18

pg_summarize:	# rust pgrx 0.19.1 (forked)
	./build pg_summarize 14 15 16 17 18

pg_tiktoken:	# rust pgrx 0.19.1
	./build pg_tiktoken 14 15 16 17 18

pg_tiktoken_c:
	./build pg_tiktoken_c 14 15 16 17 18

pg4ml:
	./build pg4ml 14 15 16 17 18

pgml:			# rust pgrx 0.12.9 (obsolete)
	./build pgml 14 15 16 17

pgmnemo:
	./build pgmnemo 17 18



###############################################################
#                       Category: FTS                         #
###############################################################
pg_search:      # rust pgrx 0.19.1
	./build pg_search 15 16 17 18

pgroonga:
	./build pgroonga 14 15 16 17 18

pg_bigm:     	# covered by PGDG (deb break on 18)
	./build pg_bigm 14 15 16 17 18

# zhparser and scws deps
scws:
	rm -rf ~/rpmbuild/RPMS/$(ARCH)/scws*.rpm /tmp/pigsty-rpm/RPMS/scws*.rpm
	QA_RPATHS=2 rpmbuild -ba ~/rpmbuild/SPECS/scws.spec
scws-install:
	sudo yum remove -y scws || /bin/true
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/scws-1.2.3-1PIGSTY.el*.$(ARCH).rpm
zhparser:
	QA_RPATHS=2 ./build zhparser 14 15 16 17 18

pg_cjk_parser:
	./build pg_cjk_parser 14 15 16 17 18

pg_jieba:
	./build pg_jieba 14 15 16 17 18

pg_bestmatch:		# rust pgrx 0.19.1
	./build pg_bestmatch 14 15 16 17 18

vchord_bm25:		# rust pgrx 0.19.1
	./build vchord_bm25 14 15 16 17 18

pg_tokenizer:		# rust pgrx 0.19.1
	./build pg_tokenizer 14 15 16 17 18

pg_biscuit:
	./build pg_biscuit 16 17 18

pg_textsearch:
	./build pg_textsearch 17 18

pg_fts:
	./build pg_fts 17 18

pg_pinyin:			# rust pgrx 0.19.1
	./build pg_pinyin 14 15 16 17 18

pg_kazsearch:		# rust pgrx 0.19.1
	./build pg_kazsearch 16 17 18

psql_bm25s:
	./build psql_bm25s 17 18

hunspell: hunspell_cs_cz hunspell_de_de hunspell_en_us hunspell_fr hunspell_ne_np hunspell_nl_nl hunspell_nn_no hunspell_ru_ru hunspell_ru_ru_aot #hunspell_pt_pt
hunspell_cs_cz:
	./build hunspell_cs_cz     14 15 16 17 18
hunspell_de_de:
	./build hunspell_de_de     14 15 16 17 18
hunspell_en_us:
	./build hunspell_en_us     14 15 16 17 18
hunspell_fr:
	./build hunspell_fr        14 15 16 17 18
hunspell_ne_np:
	./build hunspell_ne_np     14 15 16 17 18
hunspell_nl_nl:
	./build hunspell_nl_nl     14 15 16 17 18
hunspell_nn_no:
	./build hunspell_nn_no     14 15 16 17 18
hunspell_pt_pt:
	./build hunspell_pt_pt     14 15 16 17 18
hunspell_ru_ru:
	./build hunspell_ru_ru     14 15 16 17 18
hunspell_ru_ru_aot:
	./build hunspell_ru_ru_aot 14 15 16 17 18

###############################################################
#                       Category: OLAP                        #
###############################################################
citus:
	./build citus 16 17 18

hydra:
	./build hydra 14 15 16 #17 not ready yet

# DuckDB family platform policy:
# - pg_duckdb, duckdb_fdw, and pg_mooncake remain EL8/EL9/EL10 capable.
# - pg_lake requires EL9+ for system OpenSSL 3.
# - pg_ducklake is EL9+ until its EL8/GCC8 filesystem path is fixed and tested.
#pg_analytics:   # download, obsolete
pg_duckdb:
	./build pg_duckdb 14 15 16 17 18

pg_lake:                 # EL9+ only: bundled DuckDB requires system OpenSSL 3
	./build pg_lake 16 17 18

pg_mooncake:
	./build pg_mooncake 14 15 16 17 18

storage_engine:
	./build storage_engine 15 16 17 18

pg_clickhouse:
	./build pg_clickhouse 14 15 16 17 18

#duckdb_fdw:
#	./build duckdb_fdw

pg_parquet:			# rust pgrx 0.19.1
	./build pg_parquet 14 15 16 17 18

pg_ducklake:             # EL9+ only: EL8/GCC8 filesystem support is unverified
	./build pg_ducklake 14 15 16 17 18

# pg_fkpart
pg_kpart:
	./build pg_kpart 14 15 16 17 18

pg_partman:
	./build pg_partman 14 15 16 17 18

pg_orca:
	./build pg_orca 18

pg_sorted_heap:
	./build pg_sorted_heap 16 17 18

plproxy:
	./build plproxy 14 15 16 17 18
# pg_strom

###############################################################
#                       Category: FEAT                        #
###############################################################
age:
	./build age 17 18

onesparse:
	./build onesparse 18

pggraph:		# rust pgrx 0.19.1, installs graph extension
	./build pggraph 14 15 16 17 18

pgrdf:			# rust pgrx 0.19.1
	./build pgrdf 14 15 16 17 18

pgmq:
	./build pgmq 14 15 16 17 18

pgmb:
	./build pgmb 14 15 16 17 18

ulak:
	./build ulak 14 15 16 17 18

fsm_core:
	./build fsm_core 15 16 17 18

#hll:
rum:
	./build rum 16 17 18

pg_ai_query:
	./build pg_ai_query 14 15 16 17 18

pg_monetdb:		# obsolete: monetdb-devel is unavailable in active EL builder repos
	@echo "pg_monetdb is obsolete; monetdb-devel is unavailable in active EL builder repos"

pg_ilib:		# deferred: draft spec kept in SPECS/obsolete
	@echo "pg_ilib is deferred; draft spec kept in SPECS/obsolete"

pg_igraph:		# deferred: draft spec kept in SPECS/obsolete
	@echo "pg_igraph is deferred; draft spec kept in SPECS/obsolete"

pg_ttl_index:
	./build pg_ttl_index 15 16 17 18

pg_graphql:		# rust pgrx 0.19.1
	./build pg_graphql 14 15 16 17 18

pg_jsonschema:	# rust pgrx 0.19.1
	./build pg_jsonschema 14 15 16 17 18

jsonschema:		# rust pgrx 0.19.1, distinct from pg_jsonschema
	./build jsonschema 14 15 16 17 18

#jsquery:
#pg_hint_plan
index_advisor:
	./build index_advisor 14 15 16 17 18

pg_plan_filter:
	./build pg_plan_filter 14 15 16 17 18

pg_variables:
	./build pg_variables 14 15 16 17 18

imgsmlr:
	./build imgsmlr 14 15 16 17 18

pg_ivm:
	./build pg_ivm 14 15 16 17 18

pg_incremental:
	./build pg_incremental 16 17 18

pg_trickle:		# rust pgrx 0.19.1, PG18 only
	./build pg_trickle 18

pg_durable:		# rust pgrx 0.19.1, shared_preload_libraries
	./build pg_durable 14 15 16 17 18

provsql:
	./build provsql 14 15 16 17 18

# pgq

pg_cardano:
	./build pg_cardano 15 16 17 18

# rdkit
inchi:
	./build inchi 18

rdkit:
	./build rdkit 18

# omnigres
omnigres:
	./build omnigres 14 15 16 17 18

###############################################################
#                       Category: LANG                        #
###############################################################
pg_tle:
	./build pg_tle 14 15 16 17 18

plv8:
	./build plv8 14 15 16 17 18

pljs:
	./build pljs 14 15 16 17 18

plx:
	./build plx 14 15 16 17 18

plprql: 		# rust pgrx 0.19.1
	./build plprql 14 15 16 17 18

plpgsql_check:
	./build plpgsql_check 14 15 16 17 18

pg_mockable:
	./build pg_mockable 14 15 16 17 18

pgsqlmock:
	./build pgsqlmock 14 15 16 17 18

pg_typescript:		# rust pgrx 0.19.1
	./build pg_typescript 16 17 18

# pllua

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
	./build pg_prefix 14 15 16 17 18

pg_semver:
	./build pg_semver 14 15 16 17 18

pg_text_semver:
	./build pg_text_semver 14 15 16 17 18

pgunit:
	./build pgunit 14 15 16 17 18
pgpdf: 		# covered by PGDG
	./build pgpdf 14 15 16 17 18

pglite_fusion:
	./build pglite_fusion 14 15 16 17 18

md5hash:
	./build md5hash 14 15 16 17 18

asn1oid:
	./build asn1oid 14 15 16 17 18

pg_roaringbitmap:
	./build pg_roaringbitmap 14 15 16 17 18

pgfaceting:
	./build pgfaceting 14 15 16 17 18

pgsphere:
	./build pgsphere 14 15 16 17 18

pg_country:
	./build pg_country 14 15 16 17 18

pg_xenophile:
	./build pg_xenophile 14 15 16 17 18

pg_currency:
	./build pg_currency 14 15 16 17 18

pgcollection:
	./build pgcollection 14 15 16 17 18

numeral:
	./build numeral 14 15 16 17 18

pg_rational:
	./build pg_rational 14 15 16 17 18

pguint:
	./build pguint 14 15 16 17 18

pg_uint128:
	./build pg_uint128 14 15 16 17 18

hashtypes:
	./build hashtypes 14 15 16 17 18

pg_uri:
	./build pg_uri 14 15 16 17 18

pg_emailaddr:
	./build pg_emailaddr 14 15 16 17 18

pg_acl:
	./build pg_acl 14 15 16 17 18

pg_duration:
	./build pg_duration 17 18

pg_bikram_sambat:
	./build pg_bikram_sambat 14 15 16 17 18

pg_rrule:
	./build pg_rrule 14 15 16 17 18

chkpass:
	./build chkpass 14 15 16 17 18

#debversion:
#timestamp9:


###############################################################
#                       Category: UTIL                        #
###############################################################
pg_gzip:
	./build pg_gzip 14 15 16 17 18

pg_bzip:
	./build pg_bzip 14 15 16 17 18

pg_zstd:
	./build pg_zstd 14 15 16 17 18

pg_http:
	./build pg_http 14 15 16 17 18

pg_net:
	./build pg_net 14 15 16 17 18

pg_net2:
	./build pg_net2 14 15 16 17 18

pg_curl:
	./build pg_curl 14 15 16 17 18

pg_retry:
	./build pg_retry 17 18

pg_protobuf:
	./build pg_protobuf 14 15 16 17 18

pgproto:
	./build pgproto 14 15 16 17 18

pgjq:
	./build pgjq 14 15 16 17

pgjwt:
	./build pgjwt 14 15 16 17 18

pg_smtp_client:		# rust pgrx
	./build pg_smtp_client 14 15 16 17 18

pg_html5_email_address:
	./build pg_html5_email_address 14 15 16 17 18

url_encode:
	./build url_encode 14 15 16 17 18

pgsql_tweaks:
	./build pgsql_tweaks 14 15 16 17 18

pg_extra_time:
	./build pg_extra_time 14 15 16 17 18

pgpcre:
	./build pgpcre 14 15 16 17 18

re2:
	./build re2 16 17 18

icu_ext:
	./build icu_ext 14 15 16 17 18

pgqr:
	./build pgqr 14 15 16 17 18

pg_envvar:
	./build pg_envvar 14 15 16 17 18

pg_byteamagic:
	./build pg_byteamagic 14 15 16 17 18

external_file:
	./build external_file 14 15 16 17 18

pg_render:		# rust pgrx 0.19.1
	./build pg_render 14 15 16 17 18

#pg_readme

ddl_historization:
	./build ddl_historization 14 15 16 17 18

data_historization:
	./build data_historization 14 15 16 17 18

pg_schedoc:
	./build pg_schedoc 14 15 16 17 18

pg_isok:
	./build pg_isok 14 15 16 17 18

pg_hashlib:
	./build pg_hashlib 14 15 16 17 18

pg_xxhash:
	./build pg_xxhash 14 15 16 17 18

shacrypt:
	./build shacrypt 14 15 16 17 18

cryptint:
	./build cryptint 14 15 16 17 18

pg_ecdsa:
	./build pg_ecdsa 14 15 16 17 18

pgsparql:
	./build pgsparql 14 15 16 17 18


###############################################################
#                       Category: FUNC                        #
###############################################################
pg_idkit:			# rust pgrx 0.19.1
	./build pg_idkit 14 15 16 17 18

pgx_ulid:			# rust pgrx 0.19.1
	./build pgx_ulid  14 15 16 17 18

pg_uuid_v8:
	./build pg_uuid_v8 14 15 16 17 18

#pg_uuidv7

permuteseq:
	./build permuteseq 14 15 16 17 18

pg_hashids:
	./build pg_hashids 14 15 16 17 18

sequential_uuids:
	./build sequential_uuids 14 15 16 17 18

pg_typeid:
	./build pg_typeid 14 15 16 17 18

quantile:
	./build quantile 14 15 16 17 18

lower_quantile:
	./build lower_quantile 14 15 16 17 18

count_distinct:
	./build count_distinct 14 15 16 17 18

omnisketch:
	./build omnisketch 14 15 16 17 18

ddsketch:
	./build ddsketch 14 15 16 17 18

vasco:
	./build vasco 14 15 16 17 18

pgxicor:
	./build pgxicor 14 15 16 17 18

pg_weighted_statistics:
	./build pg_weighted_statistics 14 15 16 17 18

datasketches:
	./build datasketches 14 15 16 17 18

#tdigest

first_last_agg:
	./build first_last_agg 14 15 16 17 18

argm:
	./build argm 14 15 16 17 18

#extra_window_functions

floatvec:
	./build floatvec 14 15 16 17 18

aggs_for_vecs:
	./build aggs_for_vecs 14 15 16 17 18

aggs_for_arrays:
	./build aggs_for_arrays 14 15 16 17 18

pg_arraymath:
	./build pg_arraymath 14 15 16 17 18

pg_math:
	./build pg_math 14 15 16 17 18

pg_random:
	./build pg_random 14 15 16 17 18

pg_base36:
	./build pg_base36 14 15 16 17 18

pg_base62:
	./build pg_base62 14 15 16 17 18

pg_base58:		# rust pgrx 0.19.1
	./build pg_base58 14 15 16 17 18

pg_financial:
	./build pg_financial 14 15 16 17 18

pg_accumulator:
	./build pg_accumulator 14 15 16 17 18

pg_convert:		# rust pgrx 0.19.1
	./build pg_convert 14 15 16 17 18

parray_gin:
	./build parray_gin 14 15 16 17 18


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

pg_query_rewrite:
	./build pg_query_rewrite 14 15 16 17 18

online_advisor:
	./build online_advisor 14 15 16 17 18

pgmemento:
	./build pgmemento 14 15 16 17 18

pg_roast:
	./build pg_roast 14 15 16 17 18

pgfincore:
	./build pgfincore 14 15 16 17 18

pg_cooldown:
	./build pg_cooldown 14 15 16 17 18

ddlx:			# fix pgdg 18 missing
	./build ddlx 14 15 16 17 18

pglinter:
	./build pglinter 14 15 16 17 18

pgdd:			# rust pgrx 0.19.1
	./build pgdd 14 15 16 17 18

pg_strict:		# rust pgrx 0.19.1
	./build pg_strict 14 15 16 17 18

preprepare:
	./build preprepare 14 15 16 17 18

pg_upless:
	./build pg_upless 14 15 16 17 18

pgcozy:
	./build pgcozy 14 15 16 17 18

pg_orphaned:
	./build pg_orphaned 14 15 16 17 18

pg_crash:
	./build pg_crash 14 15 16 17 18

pg_cheat_funcs:
	./build pg_cheat_funcs 14 15 16 17 18

pg_fio:
	./build pg_fio 14 15 16 17 18

pg_qos:
	./build pg_qos 15 16 17 18

pg_pathcheck:	# preload-only diagnostics module for PG17/18
	./build pg_pathcheck 17 18

pg_savior:		# breaks on pg18 (fixed)
	./build pg_savior 14 15 16 17 18

pg_drop_events:
	./build pg_drop_events 14 15 16 17 18

table_log:
	./build table_log 14 15 16 17 18

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
pg_flight_recorder:
	./build pg_flight_recorder 15 16 17 18

pgmonitor:
	./build pgmonitor 14 15 16 17 18

pg_tracing:
	./build pg_tracing 14 15 16 17 18

pg_stat_ch:
	./build pg_stat_ch 16 17 18

pg_stat_backtrace:
	./build pg_stat_backtrace 14 15 16 17 18

pg_stat_monitor:
	./build pg_stat_monitor 18 # fix the missing pgdg

pg_store_plans:
	./build pg_store_plans 14 15 16 17 18

pg_track_optimizer:
	./build pg_track_optimizer 17 18

pg_datasentinel:
	./build pg_datasentinel 15 16 17 18
#bgw_replstatus
#powa

pgsentinel:
	./build pgsentinel 14 15 16 17 18

pg_ash:
	./build pg_ash 14 15 16 17 18

system_stats:
	./build system_stats 14 15 16 17 18

fbsql:
	./build fbsql 16 17 18

pg_meta:
	./build pg_meta 14 15 16 17 18

pgnodemx:
	./build pgnodemx 14 15 16 17 18

pg_sqlog:
	./build pg_sqlog 14 15 16 17 18

pgmeminfo:
	./build pgmeminfo 14 15 16 17 18

toastinfo:
	./build toastinfo 14 15 16 17 18

pg_explain_ui:		# rust pgrx 0.19.1
	./build pg_explain_ui 14 15 16 17 18

pg_relusage:
	./build pg_relusage 14 15 16 17 18

pagevis:
	./build pagevis 14 15 16 17 18


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

supautils:
	./build supautils 14 15 16 17 18

pgsodium:
	./build pgsodium 14 15 16 17 18

column_encrypt:
	./build column_encrypt 14 15 16 17 18

pg_vault:
	./build pg_vault 14 15 16 17 18

hyperion_vault:	# rust pgrx 0.19.1, PG18 only, shared_preload_libraries
	./build hyperion_vault 18

pg_session_jwt:		# rust pgrx 0.19.1
	./build pg_session_jwt 14 15 16 17 18

pg_oidc_validator_rust:	# rust pgrx 0.19.1, PostgreSQL 18 OAuth validator
	./build pg_oidc_validator_rust 18

pg_oidc_validator:	# C++23, PostgreSQL 18 OAuth validator
	./build pg_oidc_validator 18

pg_anon:			# rust pgrx 0.19.1
	./build pg_anon 14 15 16 17 18

pgsmcrypto:			# rust pgrx 0.19.1
	./build pgsmcrypto 14 15 16 17 18

pg_enigma:			# rust pgrx 0.19.1
	./build pg_enigma 14 15 16 17 18

pg_auditor:
	./build pg_auditor 14 15 16 17 18

pgcryptokey:
	./build pgcryptokey 14 15 16 17 18

login_hook:
	./build login_hook 14 15 16 17 18

pg_snakeoil:
	./build pg_snakeoil 14 15 16 17 18

pgextwlist:
	./build pgextwlist 14 15 16 17 18

pg_command_fw:		# rust pgrx 0.19.1
	./build pg_command_fw 15 16 17 18

block_copy_command:	# rust pgrx 0.19.1
	./build block_copy_command 14 15 16 17 18

sslutils:
	./build sslutils 14 15 16 17 18

pg_noset:
	./build pg_noset 14 15 16 17 18

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

wrappers:			# rust pgrx 0.19.1
	./build wrappers 14 15 16 17 18

sqlite_fdw:
	./build sqlite_fdw 14 15 16 17 18

etcd_fdw:			# rust pgrx 0.19.1
	./build etcd_fdw 14 15 16 17 18

nominatim_fdw:
	./build nominatim_fdw 14 15 16 17 18

redis_fdw:
	./build redis_fdw 14 15 16 17 18

pg_redis_pubsub:
	./build pg_redis_pubsub 14 15 16 17 18

kafka_fdw:
	./build kafka_fdw 14 15 16 17

firebird_fdw:
	./build firebird_fdw 14 15 16 17 18

aws_s3:
	./build aws_s3 14 15 16 17 18

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

pg_projection:
	./build pg_projection 14 15 16 17 18

session_variable:
	./build session_variable 14 15 16 17 18

db2fce:
	./build db2fce 14 15 16 17 18

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
	./build pglogical_ticker 14 15 16 17 #18

logical_ddl:
	./build logical_ddl 14 15 16 17 18

pg_failover_slots:
	./build pg_failover_slots 14 15 16 17 18

db_migrator:
	./build db_migrator 14 15 16 17 18

libpgfeutils:	# require perl-FindBin
	./build libpgfeutils14 14
	./build libpgfeutils15 15
	./build libpgfeutils16 16
	./build libpgfeutils17 17
	./build libpgfeutils18 18

libpgfeutils-install:
	sudo rpm -ivh ~/rpmbuild/RPMS/$(ARCH)/libpgfeutils*$(ARCH).rpm

pgactive:
	./build pgactive 14 15 16 17 18

pgclone:
	./build pgclone 14 15 16 17 18

pgmqtt:			# rust pgrx 0.19.1
	./build pgmqtt 14 15 16 17 18

decoder_raw:
	./build decoder_raw 14 15 16 17 18

mimeo:
	./build mimeo 14 15 16 17 18

pg_bulkload:
	./build pg_bulkload 14 15 16 17 18

postgresbson:
	./build postgresbson 14 15 16 17 18

###############################################################
#                          Misc                               #
###############################################################
haproxy:
	rpmbuild -ba SPECS/haproxy.spec

pdu:
	./build pdu 14 15 16 17 18

pgdog:
	rpmbuild -ba SPECS/pgdog.spec
pgdog-install:
	sudo yum remove -y pgdog || /bin/true
	sudo rpm -Uvh --replacepkgs ~/rpmbuild/RPMS/$(ARCH)/pgdog-[0-9]*.$(ARCH).rpm

pg_filedump:
	./build pg_filedump 18

###############################################################
#                       Kernels                               #
###############################################################
openhalodb:
	QA_RPATHS=3 rpmbuild -ba SPECS/openhalodb.spec
openhalo: openhalodb

ivorysql:
	QA_RPATHS=3 rpmbuild -ba SPECS/ivorysql.spec

ivorysql-contrib:
	QA_RPATHS=3 rpmbuild -ba SPECS/ivorysql-contrib.spec

ivorysql-all: ivorysql ivorysql-contrib

agensgraph:
	QA_RPATHS=3 rpmbuild -ba SPECS/agensgraph.spec

zlog:
	rpmbuild -ba SPECS/zlog.spec

polarstore:
	rpmbuild -ba SPECS/polarstore.spec

polardb:
	QA_RPATHS=3 rpmbuild -ba SPECS/polardb.spec

pgedge: pgedge-18
pgedge-18:
	QA_RPATHS=3 ./build pgedge 18
pgedge-17:
	QA_RPATHS=3 ./build pgedge 17
pgedge-16:
	QA_RPATHS=3 ./build pgedge 16
pgedge-15:
	QA_RPATHS=3 ./build pgedge 15

antlr4:
	rpmbuild -ba SPECS/antlr4-runtime413.spec

babelfish: babelfish-17
babelfish-18:
	QA_RPATHS=3 rpmbuild -ba SPECS/babelfish.spec --define "pgmajorversion 18" --define "pgversion 18.3" --define "bbfversion 6.0.0"
babelfish-17:
	QA_RPATHS=3 rpmbuild -ba SPECS/babelfish.spec --define "pgmajorversion 17" --define "pgversion 17.7" --define "bbfversion 5.4.0"

orioledb: orioledb-18
orioledb-18:
	QA_RPATHS=3 ./build orioledb 18
orioledb-17:
	QA_RPATHS=3 ./build orioledb 17
orioledb-16:
	QA_RPATHS=3 ./build orioledb 16
orioledb-all:
	QA_RPATHS=3 ./build orioledb 16 17 18

###############################################################
#                      Cloudberry Build                        #
###############################################################
cloudberry:
	QA_RPATHS=11 rpmbuild -ba SPECS/cloudberry.spec

cloudberry-backup:
	QA_RPATHS=11 rpmbuild -ba SPECS/cloudberry-backup.spec

cloudberry-pxf:
	QA_RPATHS=11 rpmbuild -ba SPECS/cloudberry-pxf.spec


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

.PHONY: env pig setup repo tool spec rust pgrx pgrx0161 pgrx0170 pgrx0180 pgrx0181 \
	pgrx0191 rust1 rust2 rust3 rust4 rust5 rust6 rust7 rust8 rust9 rust10 time haproxy timescaledb \
	timescaledb_toolkit pg_timeseries periods temporal_tables pg_task pg_later pg_background \
	pg_when pg_stl cron_utils q3c geoip pg_polyline pg_eviltransform pg_geohash pghydro pg_tzf pgvector \
	vchord pgvectorscale pg_vectorize pg_similarity pg_rrf smlar pg_summarize pg_tiktoken pg_tiktoken_c pg4ml \
	pgml pgmnemo pg_search pgroonga pg_bigm scws scws-install zhparser pg_cjk_parser pg_jieba pg_bestmatch vchord_bm25 \
	pg_tokenizer pg_biscuit pg_textsearch pg_fts pg_pinyin pg_kazsearch psql_bm25s hunspell \
	hunspell_cs_cz hunspell_de_de hunspell_en_us hunspell_fr hunspell_ne_np hunspell_nl_nl \
	hunspell_nn_no hunspell_pt_pt hunspell_ru_ru hunspell_ru_ru_aot citus hydra pg_duckdb \
	pg_lake pg_mooncake storage_engine pg_clickhouse pg_parquet pg_ducklake pg_kpart pg_partman pg_orca \
	pg_sorted_heap age onesparse pggraph pgrdf pgmq pgmb ulak fsm_core rum pg_ai_query \
	pg_monetdb pg_ilib pg_igraph pg_ttl_index pg_graphql pg_jsonschema jsonschema index_advisor \
	pg_plan_filter pg_variables imgsmlr pg_ivm pg_incremental pg_trickle pg_durable provsql fbsql \
	pg_cardano inchi rdkit pg_tle plv8 pljs plx plprql plpgsql_check pg_mockable pgsqlmock pg_typescript \
	pg_prefix pg_semver pg_text_semver pgunit pgpdf pglite_fusion md5hash asn1oid \
	pg_roaringbitmap pgfaceting pgsphere pg_country pg_xenophile pg_currency pgcollection \
	numeral pg_rational pguint pg_uint128 hashtypes pg_uri pg_emailaddr pg_acl pg_duration \
	pg_bikram_sambat pg_rrule chkpass pg_gzip pg_bzip pg_zstd pg_http pg_net pg_net2 pg_curl \
	pg_retry pg_protobuf pgproto pgjq pgjwt pg_smtp_client pg_html5_email_address url_encode \
	pgsql_tweaks pg_extra_time pgpcre re2 icu_ext pgqr pg_envvar pg_byteamagic external_file \
	pg_render ddl_historization data_historization pg_schedoc pg_isok pg_hashlib pg_xxhash \
	shacrypt cryptint pg_ecdsa pgsparql pg_idkit pgx_ulid pg_uuid_v8 permuteseq pg_hashids \
	sequential_uuids pg_typeid quantile lower_quantile count_distinct omnisketch ddsketch vasco \
	pgxicor pg_weighted_statistics datasketches first_last_agg argm floatvec aggs_for_vecs \
	aggs_for_arrays pg_arraymath pg_math pg_random pg_base36 pg_base62 pg_base58 pg_financial \
	pg_accumulator pg_convert parray_gin pg_query_rewrite online_advisor pgmemento pg_roast pgfincore pg_cooldown ddlx pglinter \
	pgdd preprepare pg_upless pgcozy pg_orphaned pg_crash pg_cheat_funcs pg_fio pg_qos \
	pg_pathcheck pg_savior pg_drop_events table_log pg_flight_recorder pgmonitor pg_tracing pg_stat_ch pg_stat_backtrace \
	pg_stat_monitor pg_store_plans pg_track_optimizer pg_datasentinel pgsentinel pg_ash \
	system_stats pg_meta pgnodemx pg_sqlog pgmeminfo toastinfo pg_explain_ui pg_relusage \
	pagevis supautils pgsodium column_encrypt pg_vault hyperion_vault pg_session_jwt pg_oidc_validator_rust pg_oidc_validator pg_anon \
	pgsmcrypto pg_enigma pg_auditor pgcryptokey login_hook pg_snakeoil pgextwlist pg_command_fw \
	block_copy_command sslutils pg_noset wrappers sqlite_fdw etcd_fdw nominatim_fdw redis_fdw \
	pg_redis_pubsub kafka_fdw firebird_fdw aws_s3 documentdb pg_projection session_variable \
	db2fce spat pglogical_ticker logical_ddl pg_failover_slots db_migrator libpgfeutils \
	libpgfeutils-install pgactive pgclone pgmqtt decoder_raw mimeo pg_bulkload postgresbson pdu \
	pgdog pgdog-install pg_filedump openhalo openhalodb ivorysql ivorysql-contrib ivorysql-all agensgraph zlog polarstore polardb \
	pgedge pgedge-15 pgedge-16 pgedge-17 pgedge-18 antlr4 babelfish babelfish-17 babelfish-18 orioledb \
	orioledb-16 orioledb-17 orioledb-18 orioledb-all cloudberry cloudberry-backup cloudberry-pxf \
	ls-rpm ls-srpm rm-rpm rm-srpm rmdbg
