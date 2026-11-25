%global pgbaseinstdir /usr/halo-19
# These libraries are private to the OpenHalo installation.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$
# Preserve per-object DWARF line tables, as for the other PG kernel bundles.
%global _find_debuginfo_dwz_opts %{nil}

Name:           openhalodb-19
Version:        19.0.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL 19 kernel with the OpenHalo MySQL protocol and SQL dialect
License:        PostgreSQL AND GPL-3.0-or-later
URL:            https://github.com/pgsty/openhalo
Source0:        https://github.com/pgsty/openhalo/archive/refs/tags/v%{version}.tar.gz#/openhalodb-%{version}.tar.gz
Patch0:         openhalodb-19.0.0-c23-noreturn.patch

BuildRequires:  gcc, gcc-c++, make, patch, bison, flex, gettext, pkgconfig
BuildRequires:  readline-devel, zlib-devel, lz4-devel, libzstd-devel, libicu-devel
BuildRequires:  libuuid-devel, libxml2-devel, libxslt-devel, openssl-devel
BuildRequires:  krb5-devel, libselinux-devel, openldap-devel, pam-devel, systemd-devel
BuildRequires:  python3-devel, tcl-devel, perl, perl-ExtUtils-Embed, perl-FindBin
BuildRequires:  systemtap-sdt-devel, llvm-devel >= 19.0, clang-devel >= 19.0
Requires:       tzdata
Requires(pre):  shadow-utils

%description
OpenHalo combines PostgreSQL 19.0 with the preloaded aux_mysql 2.0
extension. PostgreSQL and MySQL clients can read and write the same data.
The server, clients, development files, contrib modules and LLVM JIT
provider are installed together under %{pgbaseinstdir}.

%prep
%autosetup -n openhalo-%{version} -p1

%build
%set_build_flags
./configure --prefix=%{pgbaseinstdir} --libdir=%{pgbaseinstdir}/lib \
    --docdir=%{pgbaseinstdir}/doc --htmldir=%{pgbaseinstdir}/doc/html \
    --with-system-tzdata=/usr/share/zoneinfo --enable-rpath \
    --with-icu --with-llvm --with-ssl=openssl --with-uuid=e2fs \
    --with-lz4 --with-zstd --with-libxml --with-libxslt \
    --with-python --with-perl --with-tcl --with-pam --with-gssapi \
    --with-ldap --with-selinux --with-systemd --enable-nls --enable-dtrace
MAKELEVEL=0 %{__make} -C src/backend %{?_smp_mflags} submake-generated-headers
%{__make} %{?_smp_mflags} rpathdir=%{pgbaseinstdir}/lib world-bin

%install
%{__make} %{?_smp_mflags} rpathdir=%{pgbaseinstdir}/lib DESTDIR=%{buildroot} install-world-bin
cp -p contrib/aux_mysql/COPYRIGHT COPYRIGHT.aux_mysql
cp -p contrib/aux_mysql/README.md README.aux_mysql.md
# EL10 checks absolute private RUNPATHs. Allow only the path verified below.
export QA_RPATHS=0x0002
find %{buildroot}%{pgbaseinstdir} -type f \( -perm /111 -o -name '*.so*' \) \
    -exec readelf -d {} + 2>/dev/null | awk \
    '/\((RUNPATH|RPATH)\)/ && $NF != "[%{pgbaseinstdir}/lib]" {print; bad=1} END {exit bad}'

%check
prefix=%{buildroot}%{pgbaseinstdir}
test -s "$prefix/lib/postgresql/llvmjit.so"
test -s "$prefix/lib/postgresql/aux_mysql.so"
test -s "$prefix/lib/postgresql/bitcode/aux_mysql.index.bc"
test -s "$prefix/share/postgresql/extension/aux_mysql--2.0.sql"
grep -Fx "default_version = '2.0'" "$prefix/share/postgresql/extension/aux_mysql.control"
grep -q "^shared_preload_libraries = 'aux_mysql'" "$prefix/share/postgresql/postgresql.conf.sample"

%pre
getent group postgres >/dev/null || groupadd -r -g 26 postgres || groupadd -r postgres
getent passwd postgres >/dev/null || useradd -M -r -u 26 -g postgres -d /var/lib/pgsql -s /bin/bash postgres || useradd -M -r -g postgres -d /var/lib/pgsql -s /bin/bash postgres

%files
%license COPYRIGHT LICENSE 3party-legal-notices COPYRIGHT.aux_mysql
%doc README.md README.postgresql.md README.aux_mysql.md contrib/aux_mysql/MIGRATION.md
%{pgbaseinstdir}

%changelog
* Tue Nov 24 2026 Ruohang Feng <rh@vonng.com> - 19.0.0-1PGSTY
- Package OpenHalo 19.0.0 with PostgreSQL 19.0, aux_mysql 2.0 and LLVM JIT
