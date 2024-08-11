#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2024-08-10
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
	rm -rf ~/rpmbuild/RPMS/x86_64/zhparser*.rpm;
	QA_RPATHS=2 rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/zhparser.spec
	QA_RPATHS=2 rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/zhparser.spec
	QA_RPATHS=2 rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/zhparser.spec
	QA_RPATHS=2 rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/zhparser.spec
	QA_RPATHS=2 rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/zhparser.spec   # not available on el7

#---------------------------------------------#
# duckdb_fdw (depend on libduckdb)
#---------------------------------------------#
duckdb_fdw:
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/duckdb_fdw.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/duckdb_fdw.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/duckdb_fdw.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/duckdb_fdw.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/duckdb_fdw.spec

#---------------------------------------------#
# plv8 (manually build)
#---------------------------------------------#
plv8:
	rm -rf ~/rpmbuild/RPMS/x86_64/plv8*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/plv8.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/plv8.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/plv8.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/plv8.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/plv8.spec

#---------------------------------------------#
# hunspell
#---------------------------------------------#
hunspell: hunspell_cs_cz hunspell_de_de hunspell_en_us hunspell_fr hunspell_ne_np hunspell_nl_nl hunspell_nn_no hunspell_pt_pt hunspell_ru_ru hunspell_ru_ru_aot

hunspell_cs_cz:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_cs_cz*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_cs_cz.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_cs_cz.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_cs_cz.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_cs_cz.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_cs_cz.spec
hunspell_de_de:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_de_de*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_de_de.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_de_de.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_de_de.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_de_de.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_de_de.spec
hunspell_en_us:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_en_us*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_en_us.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_en_us.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_en_us.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_en_us.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_en_us.spec
hunspell_fr:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_fr*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_fr.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_fr.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_fr.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_fr.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_fr.spec
hunspell_ne_np:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_ne_np*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_ne_np.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_ne_np.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_ne_np.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_ne_np.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_ne_np.spec
hunspell_nl_nl:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_nl_nl*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_nl_nl.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_nl_nl.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_nl_nl.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_nl_nl.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_nl_nl.spec
hunspell_nn_no:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_nn_no*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_nn_no.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_nn_no.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_nn_no.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_nn_no.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_nn_no.spec
hunspell_pt_pt:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_pt_pt*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_pt_pt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_pt_pt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_pt_pt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_pt_pt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_pt_pt.spec
hunspell_ru_ru:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_ru_ru*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_ru_ru.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_ru_ru.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_ru_ru.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_ru_ru.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_ru_ru.spec
hunspell_ru_ru_aot:
	rm -rf ~/rpmbuild/RPMS/x86_64/hunspell_ru_ru_aot*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/hunspell_ru_ru_aot.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hunspell_ru_ru_aot.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hunspell_ru_ru_aot.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hunspell_ru_ru_aot.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hunspell_ru_ru_aot.spec


#---------------------------------------------#
# pg_roaringbitmap
#---------------------------------------------#
pg_roaringbitmap:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_roaringbitmap*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_roaringbitmap.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_roaringbitmap.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_roaringbitmap.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_roaringbitmap.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_roaringbitmap.spec   # not available on el7

#---------------------------------------------#
# pgjwt
#---------------------------------------------#
pgjwt:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgjwt*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgjwt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgjwt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgjwt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgjwt.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgjwt.spec

#---------------------------------------------#
# pg_sqlog
#---------------------------------------------#
pg_sqlog:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_sqlog*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_sqlog.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_sqlog.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_sqlog.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_sqlog.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_sqlog.spec

#---------------------------------------------#
# pg_hashids
#---------------------------------------------#
pg_hashids:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_hashids*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_hashids.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_hashids.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_hashids.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_hashids.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_hashids.spec

#---------------------------------------------#
# postgres_shacrypt
#---------------------------------------------#
postgres_shacrypt:
	rm -rf ~/rpmbuild/RPMS/x86_64/postgres_shacrypt*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/postgres_shacrypt.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/postgres_shacrypt.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/postgres_shacrypt.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/postgres_shacrypt.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/postgres_shacrypt.spec

#---------------------------------------------#
# permuteseq
#---------------------------------------------#
permuteseq:
	rm -rf ~/rpmbuild/RPMS/x86_64/permuteseq*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/permuteseq.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/permuteseq.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/permuteseq.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/permuteseq.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/permuteseq.spec

#---------------------------------------------#
# vault
#---------------------------------------------#
vault:
	rm -rf ~/rpmbuild/RPMS/x86_64/vault*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/vault.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/vault.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/vault.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/vault.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/vault.spec

#---------------------------------------------#
# supautils
#---------------------------------------------#
supautils:
	rm -rf ~/rpmbuild/RPMS/x86_64/supautils*.rpm;
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/supautils.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/supautils.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/supautils.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/supautils.spec

#---------------------------------------------#
# imgsmlr
#---------------------------------------------#
imgsmlr:
	rm -rf ~/rpmbuild/RPMS/x86_64/imgsmlr*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/imgsmlr.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/imgsmlr.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/imgsmlr.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/imgsmlr.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/imgsmlr.spec

#---------------------------------------------#
# pg_similarity
#---------------------------------------------#
pg_similarity:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_similarity*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_similarity.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_similarity.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_similarity.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_similarity.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_similarity.spec

#---------------------------------------------#
# hydra (lz4-devel libzstd-devel)
#---------------------------------------------#
hydra:
	rm -rf ~/rpmbuild/RPMS/x86_64/hydra*.rpm;
	PATH=/usr/pgsql-13/bin:/usr/bin/:$PATH rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/hydra.spec
	PATH=/usr/pgsql-14/bin:/usr/bin/:$PATH rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/hydra.spec
	PATH=/usr/pgsql-15/bin:/usr/bin/:$PATH rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/hydra.spec
	PATH=/usr/pgsql-16/bin:/usr/bin/:$PATH rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/hydra.spec

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
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_tde*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_tde.spec

#---------------------------------------------#
# md5hash
#---------------------------------------------#
md5hash:
	rm -rf ~/rpmbuild/RPMS/x86_64/md5hash*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/md5hash.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/md5hash.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/md5hash.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/md5hash.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/md5hash.spec



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
	rm -rf ~/rpmbuild/RPMS/x86_64/preprepare*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/preprepare.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/preprepare.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/preprepare.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/preprepare.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/preprepare.spec

#---------------------------------------------#
# first_last_agg
#---------------------------------------------#
first_last_agg:
	rm -rf ~/rpmbuild/RPMS/x86_64/first_last_agg*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/first_last_agg.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/first_last_agg.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/first_last_agg.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/first_last_agg.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/first_last_agg.spec

#---------------------------------------------#
# pgpcre
#---------------------------------------------#
pgpcre:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgpcre*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgpcre.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgpcre.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgpcre.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgpcre.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgpcre.spec

#---------------------------------------------#
# icu_ext
#---------------------------------------------#
icu_ext:
	rm -rf ~/rpmbuild/RPMS/x86_64/icu_ext*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/icu_ext.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/icu_ext.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/icu_ext.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/icu_ext.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/icu_ext.spec

#---------------------------------------------#
# asn1oid
#---------------------------------------------#
asn1oid:
	rm -rf ~/rpmbuild/RPMS/x86_64/asn1oid*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/asn1oid.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/asn1oid.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/asn1oid.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/asn1oid.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/asn1oid.spec

#---------------------------------------------#
# numeral
#---------------------------------------------#
numeral:
	rm -rf ~/rpmbuild/RPMS/x86_64/numeral*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/numeral.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/numeral.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/numeral.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/numeral.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/numeral.spec

#---------------------------------------------#
# pg_rational
#---------------------------------------------#
pg_rational:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_rational*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_rational.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_rational.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_rational.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_rational.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_rational.spec

#---------------------------------------------#
# q3c
#---------------------------------------------#
q3c:
	rm -rf ~/rpmbuild/RPMS/x86_64/q3c*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/q3c.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/q3c.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/q3c.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/q3c.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/q3c.spec

#---------------------------------------------#
# pgsphere
#---------------------------------------------#
pgsphere:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgsphere*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgsphere.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgsphere.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgsphere.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgsphere.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgsphere.spec

#---------------------------------------------#
# pgfaceting
#---------------------------------------------#
pgfaceting:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgfaceting*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgfaceting.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgfaceting.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgfaceting.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgfaceting.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgfaceting.spec

#---------------------------------------------#
# mimeo
#---------------------------------------------#
mimeo:
	rm -rf ~/rpmbuild/RPMS/x86_64/mimeo*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/mimeo.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/mimeo.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/mimeo.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/mimeo.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/mimeo.spec

#---------------------------------------------#
# table_log
#---------------------------------------------#
table_log:
	rm -rf ~/rpmbuild/RPMS/x86_64/table_log*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/table_log.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/table_log.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/table_log.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/table_log.spec
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/table_log.spec

#---------------------------------------------#
# pg_snakeoil
#---------------------------------------------#
pg_snakeoil:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_snakeoil*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_snakeoil.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_snakeoil.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_snakeoil.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_snakeoil.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_snakeoil.spec

#---------------------------------------------#
# pgextwlist
#---------------------------------------------#
pgextwlist:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgextwlist*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgextwlist.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgextwlist.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgextwlist.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgextwlist.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgextwlist.spec

#---------------------------------------------#
# toastinfo
#---------------------------------------------#
toastinfo:
	rm -rf ~/rpmbuild/RPMS/x86_64/toastinfo*.rpm;
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/toastinfo.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/toastinfo.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/toastinfo.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/toastinfo.spec
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/toastinfo.spec


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

#---------------------------------------------#
# unit (pg16 @ el8/el9)
#---------------------------------------------#
unit:
	rm -rf ~/rpmbuild/RPMS/x86_64/unit*.rpm;
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/unit.spec

#---------------------------------------------#
# mysqlcompat (pg16 @ el8/el9)
#---------------------------------------------#
#mysqlcompat:
#	rm -rf ~/rpmbuild/RPMS/x86_64/mysqlcompat*.rpm;
#	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/mysqlcompat.spec


###############################################################
#                      The 4th Batch                          #
###############################################################
batch4: pg_orphaned pgcozy decoder_raw pg_failover_slots log_fdw index_advisor pg_financial pg_savior \
	aggs_for_vecs pg_base36 pg_base62 pg_envvar pg_html5_email_address lower_quantile pg_timeit quantile pg_random \
	session_variable smlar sslutils pg_mon chkpass pg_currency pg_emailaddr pg_uri cryptint floatvec pg_auditor noset redis_fdw

pg_orphaned:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_orphaned*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_orphaned.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_orphaned.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_orphaned.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_orphaned.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_orphaned.spec
pgcozy:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgcozy*.rpm
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgcozy.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgcozy.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgcozy.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgcozy.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgcozy.spec
decoder_raw:
	rm -rf ~/rpmbuild/RPMS/x86_64/decoder_raw*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/decoder_raw.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/decoder_raw.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/decoder_raw.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/decoder_raw.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/decoder_raw.spec
pg_failover_slots:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_failover_slots*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_failover_slots.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_failover_slots.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_failover_slots.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_failover_slots.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_failover_slots.spec
log_fdw:
	rm -rf ~/rpmbuild/RPMS/x86_64/log_fdw*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/log_fdw.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/log_fdw.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/log_fdw.spec
index_advisor:
	rm -rf ~/rpmbuild/RPMS/x86_64/index_advisor*.rpm
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/index_advisor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/index_advisor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/index_advisor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/index_advisor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/index_advisor.spec
pg_financial:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_financial*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_financial.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_financial.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_financial.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_financial.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_financial.spec
pg_savior:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_savior*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_savior.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_savior.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_savior.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_savior.spec
aggs_for_vecs:
	rm -rf ~/rpmbuild/RPMS/x86_64/aggs_for_vecs*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/aggs_for_vecs.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/aggs_for_vecs.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/aggs_for_vecs.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/aggs_for_vecs.spec
pg_base36:
	rm -rf ~/rpmbuild/RPMS/x86_64/base36*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_base36.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_base36.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_base36.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_base36.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_base36.spec
pg_base62:
	rm -rf ~/rpmbuild/RPMS/x86_64/base62*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_base62.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_base62.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_base62.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_base62.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_base62.spec
pg_envvar:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_envvar*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_envvar.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_envvar.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_envvar.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_envvar.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_envvar.spec
pg_html5_email_address:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_html5_email_address*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_html5_email_address.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_html5_email_address.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_html5_email_address.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_html5_email_address.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_html5_email_address.spec
lower_quantile:
	rm -rf ~/rpmbuild/RPMS/x86_64/lower_quantile*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/lower_quantile.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/lower_quantile.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/lower_quantile.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/lower_quantile.spec
pg_timeit:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_timeit*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_timeit.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_timeit.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_timeit.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_timeit.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_timeit.spec
quantile:
	rm -rf ~/rpmbuild/RPMS/x86_64/quantile*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/quantile.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/quantile.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/quantile.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/quantile.spec
pg_random:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_random*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_random.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_random.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_random.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_random.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_random.spec
session_variable:
	rm -rf ~/rpmbuild/RPMS/x86_64/session_variable*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/session_variable.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/session_variable.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/session_variable.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/session_variable.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/session_variable.spec
smlar:
	rm -rf ~/rpmbuild/RPMS/x86_64/smlar*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/smlar.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/smlar.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/smlar.spec
sslutils:
	rm -rf ~/rpmbuild/RPMS/x86_64/sslutils*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/sslutils.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/sslutils.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/sslutils.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/sslutils.spec
pg_mon:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_mon*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_mon.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_mon.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_mon.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_mon.spec
chkpass:
	rm -rf ~/rpmbuild/RPMS/x86_64/chkpass*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/chkpass.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/chkpass.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/chkpass.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/chkpass.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/chkpass.spec
pg_currency:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_currency*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_currency.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_currency.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_currency.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_currency.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_currency.spec
pg_emailaddr:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_emailaddr*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_emailaddr.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_emailaddr.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_emailaddr.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_emailaddr.spec
pg_uri:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_uri*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_uri.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_uri.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_uri.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_uri.spec
cryptint:
	rm -rf ~/rpmbuild/RPMS/x86_64/cryptint*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/cryptint.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/cryptint.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/cryptint.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/cryptint.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/cryptint.spec
floatvec:
	rm -rf ~/rpmbuild/RPMS/x86_64/floatvec*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/floatvec.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/floatvec.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/floatvec.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/floatvec.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/floatvec.spec
pg_auditor:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_auditor*.rpm
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_auditor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_auditor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_auditor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_auditor.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_auditor.spec
noset:
	rm -rf ~/rpmbuild/RPMS/x86_64/noset*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/noset.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/noset.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/noset.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/noset.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/noset.spec
redis_fdw:
	rm -rf ~/rpmbuild/RPMS/x86_64/redis_fdw*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/redis_fdw.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/redis_fdw.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/redis_fdw.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/redis_fdw.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/redis_fdw.spec



###############################################################
#                   5th Batch Extension                       #
###############################################################
batch5: aggs_for_arrays pgqr pg_zstd url_encode pg_geohash pg_meta pg_redis_pubsub \
	pg_arraymath pagevis pg_ecdsa pg_cheat_funcs acl pg_crash pg_math \
	sequential_uuids kafka_fdw pgnodemx pg_hashlib pg_protobuf pg_country pg_fio aws_s3 firebird_fdw

aggs_for_arrays:
	rm -rf ~/rpmbuild/RPMS/x86_64/aggs_for_arrays*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/aggs_for_arrays.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/aggs_for_arrays.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/aggs_for_arrays.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/aggs_for_arrays.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/aggs_for_arrays.spec
pgqr:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgqr*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgqr.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgqr.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgqr.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgqr.spec
pg_zstd:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_zstd*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_zstd.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_zstd.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_zstd.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_zstd.spec
url_encode:
	rm -rf ~/rpmbuild/RPMS/x86_64/url_encode*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/url_encode.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/url_encode.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/url_encode.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/url_encode.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/url_encode.spec
pg_geohash:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_geohash*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_geohash.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_geohash.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_geohash.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_geohash.spec
pg_meta:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_meta*.rpm
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_meta.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_meta.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_meta.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_meta.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_meta.spec
pg_redis_pubsub:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_redis_pubsub*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_redis_pubsub.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_redis_pubsub.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_redis_pubsub.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_redis_pubsub.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_redis_pubsub.spec
pg_arraymath:
	rm -rf ~/rpmbuild/RPMS/x86_64/array_math*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_arraymath.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_arraymath.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_arraymath.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_arraymath.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_arraymath.spec
pagevis:
	rm -rf ~/rpmbuild/RPMS/x86_64/pagevis*.rpm
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pagevis.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pagevis.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pagevis.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pagevis.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pagevis.spec
pg_ecdsa:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_ecdsa*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_ecdsa.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_ecdsa.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_ecdsa.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_ecdsa.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_ecdsa.spec
pg_cheat_funcs:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_cheat_funcs*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_cheat_funcs.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_cheat_funcs.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_cheat_funcs.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_cheat_funcs.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_cheat_funcs.spec
acl:
	rm -rf ~/rpmbuild/RPMS/x86_64/acl*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/acl.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/acl.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/acl.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/acl.spec
pg_crash:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_crash*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_crash.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_crash.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_crash.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_crash.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_crash.spec
pg_math:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_math*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_math.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_math.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_math.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_math.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_math.spec

firebird_fdw:
	rm -rf ~/rpmbuild/RPMS/x86_64/firebird_fdw*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/firebird_fdw.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/firebird_fdw.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/firebird_fdw.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/firebird_fdw.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/firebird_fdw.spec
sequential_uuids:
	rm -rf ~/rpmbuild/RPMS/x86_64/sequential_uuids*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/sequential_uuids.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/sequential_uuids.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/sequential_uuids.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/sequential_uuids.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/sequential_uuids.spec
kafka_fdw:
	rm -rf ~/rpmbuild/RPMS/x86_64/kafka_fdw*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/kafka_fdw.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/kafka_fdw.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/kafka_fdw.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/kafka_fdw.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/kafka_fdw.spec
pgnodemx:
	rm -rf ~/rpmbuild/RPMS/x86_64/pgnodemx*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pgnodemx.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pgnodemx.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pgnodemx.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pgnodemx.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pgnodemx.spec
pg_hashlib:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_hashlib*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_hashlib.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_hashlib.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_hashlib.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_hashlib.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_hashlib.spec
pg_protobuf:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_protobuf*.rpm
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_protobuf.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_protobuf.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_protobuf.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_protobuf.spec
pg_country:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_country*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_country.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_country.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_country.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_country.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_country.spec
pg_fio:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_fio*.rpm
	rpmbuild --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_fio.spec
	rpmbuild --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_fio.spec
	rpmbuild --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_fio.spec
	rpmbuild --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/pg_fio.spec
	rpmbuild --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/pg_fio.spec
aws_s3:
	rm -rf ~/rpmbuild/RPMS/x86_64/aws_s3*.rpm
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/aws_s3.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/aws_s3.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/aws_s3.spec
	rpmbuild --without debuginfo --define "pgmajorversion 13" -ba ~/rpmbuild/SPECS/aws_s3.spec
	rpmbuild --without debuginfo --define "pgmajorversion 12" -ba ~/rpmbuild/SPECS/aws_s3.spec


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
# pg_graphql [RUST]
#---------------------------------------------#
pg_graphql:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_graphql*.rpm;
	rpmbuild --without debuginfo --define "pgmajorversion 16" -ba ~/rpmbuild/SPECS/pg_graphql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 15" -ba ~/rpmbuild/SPECS/pg_graphql.spec
	rpmbuild --without debuginfo --define "pgmajorversion 14" -ba ~/rpmbuild/SPECS/pg_graphql.spec

#---------------------------------------------#
# pg_jsonschema [RUST]
#---------------------------------------------#
pg_jsonschema:
	rm -rf ~/rpmbuild/RPMS/x86_64/pg_jsonschema*.rpm;
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
	common zhparser duckdb_fdw hunspell pg_roaringbitmap pgjwt pg_sqlog pg_hashids postgres_shacrypt permuteseq	vault supautils imgsmlr pg_similarity hydra age age15 pg_tde md5hash plv8 \
	rust pg_search pg_lakehouse pg_graphql pg_jsonschema wrappers pgmq pg_vectorize pg_later plprql pg_idkit pgsmcrypto pgvectorscale # pgdd pg_tiktoken pgml \
	debian preprepare first_last_agg pgpcre icu_ext asn1oid numeral pg_rational q3c pgsphere pg_rrule pgfaceting mimeo table_log pg_snakeoil pgextwlist toastinfo \
	ls-rpm ls-srpm rm-rpm rm-srpm
