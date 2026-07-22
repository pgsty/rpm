%global sname pgtde
%global pgmajorversion 18
%global pgversion 18.4
%global perconarelease 2
%global pgtdeversion 2.2.1
%global postgisversion 3.5.7
%global pgvectorversion 0.8.3
%global wal2jsonversion 2.6
%global pgrepackversion 1.5.3
%global pgauditversion 18.0
%global setuserversion 4.2.0
%global pgstatmonitorversion 2.3.2
%global pggatherversion 33
%global pgbaseinstdir /usr/pgtde-%{pgmajorversion}

%define debug_package %{nil}
%define _build_id_links none

# Private PostgreSQL ABI under a flavor prefix, not a system libpq provider.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$

Name:           %{sname}-%{pgmajorversion}
Version:        %{pgversion}
Release:        2PIGSTY%{?dist}
Summary:        Percona PostgreSQL kernel with transparent data encryption
License:        PostgreSQL AND GPL-2.0-or-later AND GPL-3.0-only AND BSD-3-Clause
URL:            https://www.percona.com/postgresql/software/postgresql-distribution
Source0:        percona-postgresql-%{pgversion}.tar.gz
Source1:        percona-pg_tde%{pgmajorversion}-%{pgtdeversion}.tar.gz
Source2:        pgtde-pg-config
Source3:        percona-postgis-%{postgisversion}.tar.gz
Source4:        percona-pgvector_%{pgmajorversion}-%{pgvectorversion}.tar.gz
Source5:        percona-wal2json-%{wal2jsonversion}.tar.gz
Source6:        percona-pg_repack-%{pgrepackversion}.tar.gz
Source7:        percona-pgaudit-%{pgauditversion}.tar.gz
Source8:        percona-pgaudit%{pgmajorversion}_set_user-%{setuserversion}.tar.gz
Source9:        percona-pg-stat-monitor%{pgmajorversion}-%{pgstatmonitorversion}.tar.gz
Source10:       percona-pg_gather-%{pggatherversion}.tar.gz
Source11:       pgtde-sfcgal-config

ExclusiveArch:  aarch64 x86_64

BuildRequires:  glibc-devel bison flex gettext chrpath gcc gcc-c++ make patch
BuildRequires:  readline-devel zlib-devel libselinux-devel libxml2-devel libxslt-devel
BuildRequires:  libuuid-devel lz4-devel libzstd-devel libicu-devel openldap-devel
BuildRequires:  pam-devel krb5-devel python3-devel tcl-devel systemtap-sdt-devel
BuildRequires:  openssl-devel systemd-devel libcurl-devel liburing-devel json-c-devel
BuildRequires:  meson ninja-build pkgconf-pkg-config
BuildRequires:  perl perl-ExtUtils-Embed
# PostGIS dependencies. Pigsty builders resolve these from the OS, EPEL, and
# PGDG repositories; the private PostgreSQL ABI itself remains self-contained.
BuildRequires:  autoconf automake libtool gmp-devel pcre2-devel
BuildRequires:  geos-devel proj-devel libgeotiff-devel gdal-devel
BuildRequires:  SFCGAL-devel protobuf-c-devel xerces-c-devel
Requires:       tzdata
Requires(pre):  shadow-utils

%description
Pigsty private-prefix build of Percona Server for PostgreSQL %{pgversion}.%{perconarelease}
with pg_tde %{pgtdeversion}. The server, clients, development files, PGXS,
procedural languages, pg_tde, and TDE-aware PostgreSQL utilities are installed
below %{pgbaseinstdir}. The utilities use their canonical PostgreSQL names.

%package contrib
Summary:        Percona PostgreSQL extensions for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       perl-DBD-Pg

%description contrib
The PostgreSQL bundled contrib modules and the Percona Distribution for
PostgreSQL 18 key extension set: PostGIS (including client and utils),
pgvector, wal2json, pg_repack, pgaudit, pgaudit set_user, pg_stat_monitor,
and pg_gather. pg_tde is intentionally part of the main %{name} package.

%prep
%setup -q -n percona-postgresql-%{pgversion}
%{__tar} -xzf %{SOURCE1}
%{__mv} percona-pg_tde%{pgmajorversion}-%{pgtdeversion} .pg_tde-src
%{__tar} -xzf %{SOURCE3}
%{__mv} percona-postgis-%{postgisversion} .postgis-src
%{__tar} -xzf %{SOURCE4}
%{__mv} percona-pgvector_%{pgmajorversion}-%{pgvectorversion} .pgvector-src
%{__tar} -xzf %{SOURCE5}
%{__mv} percona-wal2json-%{wal2jsonversion} .wal2json-src
%{__tar} -xzf %{SOURCE6}
%{__mv} percona-pg_repack-%{pgrepackversion} .pg_repack-src
patch -d .pg_repack-src -p1 --forward -f < \
  %{_specdir}/patches/pg_repack-%{pgrepackversion}-preserve-table-am.patch
%{__tar} -xzf %{SOURCE7}
%{__mv} percona-pgaudit-%{pgauditversion} .pgaudit-src
%{__tar} -xzf %{SOURCE8}
%{__mv} percona-pgaudit%{pgmajorversion}_set_user-%{setuserversion} .set_user-src
%{__tar} -xzf %{SOURCE9}
%{__mv} percona-pg-stat-monitor%{pgmajorversion}-%{pgstatmonitorversion} .pg_stat_monitor-src
%{__tar} -xzf %{SOURCE10}
%{__mv} percona-pg_gather-%{pggatherversion} .pg_gather-src
%{__cp} -p %{SOURCE2} .pgtde-pg-config
%{__chmod} 0755 .pgtde-pg-config
%{__cp} -p %{SOURCE11} .pgtde-sfcgal-config
%{__chmod} 0755 .pgtde-sfcgal-config

%build
CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo "$CFLAGS" | xargs -n 1 | grep -v ffast-math | xargs -n 100`
LDFLAGS="-Wl,--as-needed"
export CFLAGS LDFLAGS

./configure --enable-rpath \
--prefix=%{pgbaseinstdir} \
--includedir=%{pgbaseinstdir}/include \
--mandir=%{pgbaseinstdir}/share/man \
--datadir=%{pgbaseinstdir}/share \
--libdir=%{pgbaseinstdir}/lib \
--docdir=%{pgbaseinstdir}/doc \
--htmldir=%{pgbaseinstdir}/doc/html \
--with-system-tzdata=/usr/share/zoneinfo \
--with-lz4 \
--with-zstd \
--with-uuid=e2fs \
--with-libxml \
--with-libxslt \
--with-icu \
--with-gssapi \
--with-liburing \
--without-llvm \
--with-python \
--with-perl \
--with-tcl \
--with-openssl \
--with-pam \
--with-ldap \
--with-selinux \
--with-systemd \
--with-libcurl \
--with-includes=/usr/include \
--enable-nls \
--enable-dtrace

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin

# Install the kernel and procedural languages separately from contrib so the
# two binary package payloads have an unambiguous boundary.
export PGTDE_STAGE="$(pwd)/.pgtde-stage"
export PGTDE_CONTRIB_STAGE="$(pwd)/.pgtde-contrib-stage"
%{__rm} -rf "$PGTDE_STAGE" "$PGTDE_CONTRIB_STAGE"
%{__mkdir_p} "$PGTDE_STAGE" "$PGTDE_CONTRIB_STAGE"
%{__make} DESTDIR="$PGTDE_STAGE" %{?_smp_mflags} install
%{__make} -C contrib DESTDIR="$PGTDE_CONTRIB_STAGE" %{?_smp_mflags} install

# pg_tde is part of the main package. Its Meson build needs staged headers and
# libraries, so use the build-only pg_config wrapper.
PGTDE_PG_CONFIG_MODE=stage meson setup .pgtde-build .pg_tde-src \
  --buildtype=release \
  -Dpg_config="$(pwd)/.pgtde-pg-config"
meson compile -C .pgtde-build
meson install -C .pgtde-build

%{__install} -D -m 0644 \
  .pg_tde-src/ci_scripts/perl/PostgreSQL/Test/TdeCluster.pm \
  "$PGTDE_STAGE%{pgbaseinstdir}/lib/postgresql/pgxs/src/test/perl/PostgreSQL/Test/TdeCluster.pm"

find "$PGTDE_STAGE%{pgbaseinstdir}" -type f \
  \( -name 'pg_tde*' -o -name 'pg_tde.so' \) -perm /111 -print0 | \
  xargs -0 -r -n 1 chrpath --replace %{pgbaseinstdir}/lib 2>/dev/null || :

# Build Percona's tested PG18 extension set from the Source0 archives carried
# by its 18.4 source RPMs. The wrapper resolves compile inputs inside the
# staged kernel while retaining final installation directories for DESTDIR.
export PGTDE_BUILD_PG_CONFIG="$(pwd)/.pgtde-pg-config"
export CPPFLAGS="-I$PGTDE_STAGE%{pgbaseinstdir}/include/server -I$PGTDE_STAGE%{pgbaseinstdir}/include ${CPPFLAGS:-}"
export LDFLAGS="-L$PGTDE_STAGE%{pgbaseinstdir}/lib -Wl,-rpath,%{pgbaseinstdir}/lib -Wl,--as-needed"

build_pgxs() {
  srcdir="$1"
  MAKELEVEL=0 %{__make} -C "$srcdir" %{?_smp_mflags} \
    USE_PGXS=1 PG_CONFIG="$PGTDE_BUILD_PG_CONFIG"
  MAKELEVEL=0 %{__make} -C "$srcdir" \
    USE_PGXS=1 PG_CONFIG="$PGTDE_BUILD_PG_CONFIG" \
    DESTDIR="$PGTDE_CONTRIB_STAGE" install
}

build_pgxs .pgvector-src
build_pgxs .wal2json-src
build_pgxs .pg_repack-src
build_pgxs .pgaudit-src
build_pgxs .set_user-src
build_pgxs .pg_stat_monitor-src

cd .postgis-src
./autogen.sh
CPPFLAGS="$CPPFLAGS" LDFLAGS="$LDFLAGS" ./configure \
  --prefix=%{pgbaseinstdir} \
  --bindir=%{pgbaseinstdir}/bin \
  --datadir=%{pgbaseinstdir}/share/postgresql \
  --libdir=%{pgbaseinstdir}/lib/postgresql \
  --mandir=%{pgbaseinstdir}/share/man \
  --with-pgconfig="$PGTDE_BUILD_PG_CONFIG" \
  --with-sfcgal="$(pwd)/../.pgtde-sfcgal-config" \
  --with-protobuf \
  --without-gui \
  --enable-rpath
%{__make} %{?_smp_mflags}
%{__make} DESTDIR="$PGTDE_CONTRIB_STAGE" install
%{__install} -d "$PGTDE_CONTRIB_STAGE%{pgbaseinstdir}/share/postgresql/postgis-utils"
%{__install} -m 0755 utils/*.pl \
  "$PGTDE_CONTRIB_STAGE%{pgbaseinstdir}/share/postgresql/postgis-utils/"
cd ..

# A few PGXS projects use build-time include/doc queries as install targets.
# Merge those files out of the duplicated absolute stage root, then require a
# single usr/ payload root before packaging.
nested_stage="$PGTDE_CONTRIB_STAGE$PGTDE_STAGE"
if test -d "$nested_stage"; then
  %{__cp} -a "$nested_stage/." "$PGTDE_CONTRIB_STAGE/"
fi
find "$PGTDE_CONTRIB_STAGE" -mindepth 1 -maxdepth 1 ! -name usr \
  -exec %{__rm} -rf -- {} +

# PostGIS emits DT_RPATH for its client tools. Keep private libpq discoverable
# without an RPM-invalid custom absolute RPATH.
find "$PGTDE_CONTRIB_STAGE%{pgbaseinstdir}/bin" -type f -perm /111 -print0 | \
  xargs -0 -r -n 1 chrpath --replace '$ORIGIN/../lib' 2>/dev/null || :
find "$PGTDE_CONTRIB_STAGE%{pgbaseinstdir}/lib/postgresql" \
  -type f -name '*.so' -print0 | \
  xargs -0 -r -n 1 chrpath --delete 2>/dev/null || :

%{__install} -D -m 0644 .pg_gather-src/gather.sql \
  "$PGTDE_CONTRIB_STAGE%{pgbaseinstdir}/share/postgresql/contrib/gather.sql"

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}
%{__cp} -a .pgtde-stage/usr %{buildroot}/
%{__cp} -a .pgtde-contrib-stage/usr %{buildroot}/
%{__install} -D -m 0644 COPYRIGHT \
  %{buildroot}%{_licensedir}/%{name}/core-COPYRIGHT
%{__install} -D -m 0644 .pg_tde-src/COPYRIGHT \
  %{buildroot}%{_licensedir}/%{name}/pg_tde-COPYRIGHT
%{__install} -D -m 0644 .postgis-src/COPYING \
  %{buildroot}%{_licensedir}/%{name}-contrib/postgis-COPYING
%{__install} -D -m 0644 .postgis-src/LICENSE.TXT \
  %{buildroot}%{_licensedir}/%{name}-contrib/postgis-LICENSE
for license_source in \
  pgvector:.pgvector-src/LICENSE \
  wal2json:.wal2json-src/LICENSE \
  pg_repack:.pg_repack-src/COPYRIGHT \
  pgaudit:.pgaudit-src/LICENSE \
  set_user:.set_user-src/LICENSE \
  pg_stat_monitor:.pg_stat_monitor-src/LICENSE; do
  license_name=${license_source%%:*}
  license_path=${license_source#*:}
  %{__install} -D -m 0644 "$license_path" \
    "%{buildroot}%{_licensedir}/%{name}-contrib/${license_name}-LICENSE"
done
find "%{buildroot}%{pgbaseinstdir}/lib/postgresql" \
  -type f -name '*.so' -print0 | \
  xargs -0 -r -n 1 chrpath --delete 2>/dev/null || :

# A private PostgreSQL flavor must make its TDE-aware utilities the safe
# defaults. Retain Percona's names as compatibility symlinks.
for mapping in \
  pg_tde_basebackup:pg_basebackup \
  pg_tde_checksums:pg_checksums \
  pg_tde_resetwal:pg_resetwal \
  pg_tde_rewind:pg_rewind \
  pg_tde_waldump:pg_waldump \
  pg_tde_upgrade:pg_upgrade; do
  source_name=${mapping%%:*}
  target_name=${mapping##*:}
  test -x "%{buildroot}%{pgbaseinstdir}/bin/${source_name}"
  %{__mv} -f \
    "%{buildroot}%{pgbaseinstdir}/bin/${source_name}" \
    "%{buildroot}%{pgbaseinstdir}/bin/${target_name}"
  ln -s "${target_name}" "%{buildroot}%{pgbaseinstdir}/bin/${source_name}"
done

# The main manifest owns its complete directory tree. The contrib manifest
# only lists files and symlinks, avoiding duplicate directory ownership.
(cd .pgtde-stage && find .%{pgbaseinstdir} -mindepth 1 \
  -type d -printf '%%%%dir %{pgbaseinstdir}/%%P\n'; \
  find .%{pgbaseinstdir} -mindepth 1 ! -type d \
  -printf '%{pgbaseinstdir}/%%P\n') | sort \
  > pgtde-main.files
(cd .pgtde-contrib-stage && find .%{pgbaseinstdir} -mindepth 1 \
  \( -type f -o -type l \) -printf '%{pgbaseinstdir}/%%P\n' | sort) \
  > pgtde-contrib.files

%check
test ! -e .pgtde-contrib-stage/root
test "$({ .pgtde-stage%{pgbaseinstdir}/bin/pg_config --version; })" = \
  "PostgreSQL %{pgversion} - Percona Server for PostgreSQL %{pgversion}.%{perconarelease}"
test -f %{buildroot}%{pgbaseinstdir}/lib/postgresql/pg_tde.so
test -f %{buildroot}%{pgbaseinstdir}/share/postgresql/extension/pg_tde.control
for extension in \
  postgis postgis_raster postgis_sfcgal postgis_tiger_geocoder postgis_topology \
  address_standardizer address_standardizer_data_us vector pg_repack pgaudit \
  set_user pg_stat_monitor; do
  test -f "%{buildroot}%{pgbaseinstdir}/share/postgresql/extension/${extension}.control"
done
test -x %{buildroot}%{pgbaseinstdir}/bin/pg_repack
test -x %{buildroot}%{pgbaseinstdir}/bin/shp2pgsql
test -f %{buildroot}%{pgbaseinstdir}/lib/postgresql/wal2json.so
test -f %{buildroot}%{pgbaseinstdir}/share/postgresql/contrib/gather.sql
test "$(find %{buildroot}%{pgbaseinstdir}/share/postgresql/extension \
  -maxdepth 1 -name '*.control' | wc -l)" -ge 70
for mapping in \
  pg_tde_basebackup:pg_basebackup \
  pg_tde_checksums:pg_checksums \
  pg_tde_resetwal:pg_resetwal \
  pg_tde_rewind:pg_rewind \
  pg_tde_waldump:pg_waldump \
  pg_tde_upgrade:pg_upgrade; do
  source_name=${mapping%%:*}
  target_name=${mapping##*:}
  test -x "%{buildroot}%{pgbaseinstdir}/bin/${target_name}"
  test "$(readlink "%{buildroot}%{pgbaseinstdir}/bin/${source_name}")" = "${target_name}"
done

%files -f pgtde-main.files
%doc README* HISTORY
%license %{_licensedir}/%{name}/*

%files contrib -f pgtde-contrib.files
%doc .postgis-src/README.postgis .pgvector-src/README.md .pg_repack-src/README.rst
%license %{_licensedir}/%{name}-contrib/*

%pre
getent group postgres >/dev/null 2>&1 || groupadd -g 26 -r postgres >/dev/null 2>&1 || groupadd -r postgres >/dev/null 2>&1 || :
getent passwd postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" postgres >/dev/null 2>&1 || :

%changelog
* Wed Jul 22 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 18.4-2PIGSTY
- Move pg_tde into the main kernel package
- Bundle the Percona PostgreSQL 18 key extension set in the contrib package
- Preserve the source table access method when pg_repack rebuilds TDE tables

* Wed Jul 22 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 18.4-1PIGSTY
- Add the Percona PostgreSQL 18.4.2 kernel and pg_tde 2.2.1 under /usr/pgtde-18
- Promote TDE-aware frontend tools to canonical PostgreSQL command names
