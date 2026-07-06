%global sname ivorysql-18
%global pgmajorversion 18
%global pgversion 18.4
%global ivoryversion 5.4
%global pgbaseinstdir /usr/ivory-18
# Private PostgreSQL ABI under a fork prefix, not a system libpq provider.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$
%global ivory_contrib ivorysql_ora ora_btree_gin ora_btree_gist

%define debug_package %{nil}
%define _build_id_links none

Name:           %{sname}
Version:        %{ivoryversion}
Release:        1PIGSTY%{?dist}
Summary:        IvorySQL %{ivoryversion} PostgreSQL %{pgmajorversion} kernel
License:        Apache-2.0 AND PostgreSQL
URL:            https://github.com/IvorySQL/IvorySQL
Source0:        ivorysql-%{ivoryversion}.tar.gz

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  liburing-devel, numactl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel, krb5-devel
BuildRequires:  clang, llvm, clang-devel, llvm-devel
%if 0%{?rhel} >= 10
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin, perl-interpreter
%elif 0%{?rhel} == 9
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
%else
BuildRequires:  perl-interpreter < 4:5.30
%endif
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, liburing, numactl-libs, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2, tzdata
Requires:       krb5-libs, openldap, pam, readline, zlib
Requires(pre):  shadow-utils

%description
IvorySQL %{ivoryversion} is an Oracle-compatible PostgreSQL fork based on
PostgreSQL %{pgversion}. This package ships a single complete IvorySQL
runtime, development headers, PGXS files, and bundled contrib extensions under
%{pgbaseinstdir}.

%prep
%setup -q -c -T
tar --strip-components=1 -xzf %{SOURCE0}

%build
CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo $CFLAGS | xargs -n 1 | grep -v ffast-math | xargs -n 100`
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
export CFLAGS

./configure --enable-rpath \
--prefix=%{pgbaseinstdir} \
--bindir=%{pgbaseinstdir}/bin \
--includedir=%{pgbaseinstdir}/include \
--mandir=%{pgbaseinstdir}/share/man \
--datadir=%{pgbaseinstdir}/share \
--libdir=%{pgbaseinstdir}/lib \
--docdir=%{pgbaseinstdir}/doc \
--htmldir=%{pgbaseinstdir}/doc/html \
--with-extra-version=" (IvorySQL %{ivoryversion})" \
--with-system-tzdata=/usr/share/zoneinfo \
--with-lz4 \
--with-zstd \
--with-liburing \
--with-libnuma \
--with-uuid=e2fs \
--with-libxml \
--with-libxslt \
--with-icu \
--with-llvm \
--with-gssapi \
--with-perl \
--with-python \
--with-tcl \
--with-openssl \
--with-pam \
--with-ldap \
--with-selinux \
--with-systemd \
--with-includes=/usr/include \
--with-libraries=%{_libdir} \
--enable-nls \
--enable-dtrace

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin
MAKELEVEL=0 %{__make} %{?_smp_mflags} -C contrib
for dir in %{ivory_contrib}; do
    MAKELEVEL=0 %{__make} %{?_smp_mflags} -C contrib/${dir}
done

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} -C contrib install
for dir in %{ivory_contrib}; do
    %{__make} DESTDIR=%{buildroot} VERBOSE=1 -C contrib/${dir} install
done

%files
%doc README.md README_CN.md HISTORY Notice
%license COPYRIGHT LICENSE
%{pgbaseinstdir}/lib/*
%{pgbaseinstdir}/bin/*
%{pgbaseinstdir}/share/*
%{pgbaseinstdir}/include/*
%doc %{pgbaseinstdir}/doc/*

%pre
getent group postgres >/dev/null 2>&1 || groupadd -g 26 -r postgres >/dev/null 2>&1 || groupadd -r postgres >/dev/null 2>&1 || :
getent passwd postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Sun Jul 05 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 5.4-1PIGSTY
- Add IvorySQL 5.4 PostgreSQL 18 kernel package
- Build a single complete package under /usr/ivory-18 with PGDG-like options
