%global sname orioledb
%define debug_package %{nil}
%define _build_id_links none
%{!?pgmajorversion:%global pgmajorversion 18}
%if 0%{?pgmajorversion} == 18
%global orioledb_patchset 1
%global upstream_pgver 18.4
%else
%if 0%{?pgmajorversion} == 17
%global orioledb_patchset 20
%global upstream_pgver 17.9
%else
%if 0%{?pgmajorversion} == 16
%global orioledb_patchset 47
%global upstream_pgver 16.13
%else
%{error:orioledb beta16 packaging supports PostgreSQL 16, 17, and 18 only}
%endif
%endif
%endif
%global pgbaseinstdir	/usr/oriole-%{pgmajorversion}
%global orioledb_beta beta16
%global srcdir postgres-patches%{pgmajorversion}_%{orioledb_patchset}
# Private PostgreSQL ABI under a fork prefix, not a system libpq provider.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$

Name:		%{sname}-%{pgmajorversion}
Version:	1.8
Release:	beta16PIGSTY%{?dist}
Summary:	OrioleDB PostgreSQL kernel with bundled storage engine extension
License:	PostgreSQL
URL:		https://github.com/orioledb/orioledb
Source0:	%{srcdir}.tar.gz
Source1:	%{sname}-%{orioledb_beta}.tar.gz
Patch0:		oriolepg-postgresql-branding.patch

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35, chrpath
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel, libcurl-devel
%if 0%{?rhel} >= 10
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin, perl-interpreter
%elif 0%{?rhel} == 9
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
%else
BuildRequires:  perl-interpreter < 4:5.30
%endif
Requires:       tzdata
Requires(pre):  shadow-utils

%description
OrioleDB is a modern cloud-native storage engine for PostgreSQL.
This package bundles the patched PostgreSQL %{pgmajorversion} kernel and the
OrioleDB %{version} %{orioledb_beta} extension under %{pgbaseinstdir}.
It is based on PostgreSQL %{upstream_pgver} and upstream OrioleDB patchset
%{orioledb_patchset}.

%prep
%setup -q -n %{srcdir}
%patch -P 0 -p1

rm -rf .orioledb-src contrib/orioledb
mkdir -p .orioledb-src
tar -xzf %{SOURCE1} -C .orioledb-src
orioledb_src=$(find .orioledb-src -mindepth 1 -maxdepth 1 -type d | head -n 1)
if [ -z "$orioledb_src" ]; then
  echo "cannot locate extracted OrioleDB source tree" >&2
  exit 1
fi
mv "$orioledb_src" contrib/orioledb

sed -ri 's/^([[:space:]]*)vacuumlo$/\1orioledb\t\\\n\1vacuumlo/' contrib/Makefile

%build
CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
export CFLAGS

./configure --enable-rpath \
--prefix=%{pgbaseinstdir} \
--includedir=%{pgbaseinstdir}/include \
--mandir=%{pgbaseinstdir}/share/man \
--datadir=%{pgbaseinstdir}/share \
--libdir=%{pgbaseinstdir}/lib \
--docdir=%{pgbaseinstdir}/doc \
--htmldir=%{pgbaseinstdir}/doc/html \
--with-system-tzdata=/usr/share/zoneinfo \
--with-extra-version=" (OrioleDB %{version}-%{orioledb_beta})" \
--with-lz4 \
--with-zstd \
--with-uuid=e2fs \
--with-libxml \
--with-libxslt \
--with-icu \
--without-llvm \
--with-python \
--with-tcl \
--with-openssl \
--with-pam \
--with-ldap \
--with-selinux \
--with-systemd \
--with-includes=/usr/include \
--enable-nls \
--enable-dtrace

# Source tarball build has no git metadata, force patchset for contrib/orioledb.
sed -ri 's|^ORIOLEDB_PATCHSET_VERSION =.*|ORIOLEDB_PATCHSET_VERSION = %{orioledb_patchset}|' src/Makefile.global

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin
for library in %{buildroot}%{pgbaseinstdir}/lib/postgresql/*plpython3*.so; do
  [ -e "$library" ] && chrpath -d "$library" || :
done

%files
%doc README* HISTORY
%license COPYRIGHT
%license contrib/orioledb/LICENSE-APACHE.txt contrib/orioledb/LICENSE-POSTGRESQL.txt
%{pgbaseinstdir}/lib/*
%{pgbaseinstdir}/bin/*
%{pgbaseinstdir}/share/*
%{pgbaseinstdir}/include/*
%doc %{pgbaseinstdir}/doc/*

%pre
getent group postgres >/dev/null 2>&1 || groupadd -g 26 -r postgres >/dev/null 2>&1 || groupadd -r postgres >/dev/null 2>&1 || :
getent passwd postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" postgres >/dev/null 2>&1 || :

%changelog
* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.8-beta16PIGSTY
- Merge the OriolePG kernel and OrioleDB extension into bundled orioledb packages
- Rename package output to orioledb-PGMAJOR

* Fri Jun 19 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.8-beta16PIGSTY
- Update to upstream beta16
- Require matching OriolePG beta16 patchsets for PG16/PG17/PG18

* Thu Apr 16 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.7-0.beta15PIGSTY
- Update to upstream beta15
- Require OriolePG 17.18 built from the PostgreSQL 17.7-based OrioleDB patchset

* Thu Feb 26 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.6-0.beta14PIGSTY
* Thu Jul 24 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.5-0.beta12PIGSTY
* Tue May 27 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.4-0.beta11PIGSTY
* Sat Apr 05 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.4-0.beta10PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
