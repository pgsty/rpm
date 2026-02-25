%global sname agensgraph
%global pgmajorversion 16
%global pgbaseinstdir /usr/agens-%{pgmajorversion}
%define debug_package %{nil}

Name:           %{sname}_%{pgmajorversion}
Version:        2.16.0
Release:        1PIGSTY%{?dist}
Summary:        AgensGraph kernel (PG%{pgmajorversion} fork)
License:        PostgreSQL
URL:            https://github.com/skaiworldwide-oss/agensgraph
Source0:        %{sname}-%{version}.tar.gz

BuildRequires:  glibc-devel, gettext >= 0.10.35
BuildRequires:  gcc-c++, zlib-devel >= 1.0.4
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel
BuildRequires:  bison >= 2.3, flex >= 2.5.35, readline-devel, pam-devel
%if 0%{?rhel} >= 10
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin, perl-interpreter
Requires:       systemd, lz4-libs, libzstd >= 1.5.1, /sbin/ldconfig, libicu, openssl-libs >= 3.0.0, libxml2
%elif 0%{?rhel} == 9
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2
%else
BuildRequires:  /usr/bin/perl
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2
%endif
Requires(pre):  shadow-utils

%description
AgensGraph patched PostgreSQL %{pgmajorversion} kernel package.
This package installs PostgreSQL binaries and libraries under %{pgbaseinstdir}.

%prep
%setup -q -n %{sname}-%{version}
# meta is SQL-only extension, remove mistaken MODULE_big to avoid install failure
sed -i '/^MODULE_big[[:space:]]*=[[:space:]]*meta$/d' contrib/meta/Makefile

%build
CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo $CFLAGS | xargs -n 1 | grep -v ffast-math | xargs -n 100`
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
--with-lz4 \
--with-zstd \
--with-uuid=e2fs \
--with-libxml \
--with-libxslt \
--with-icu \
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

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin

%files
%doc README.md
%license COPYRIGHT
%{pgbaseinstdir}/lib/*
%{pgbaseinstdir}/bin/*
%{pgbaseinstdir}/share/*
%{pgbaseinstdir}/include/*
%doc %{pgbaseinstdir}/doc/*

%pre
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Tue Feb 24 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 2.16.0-1PIGSTY
- Initial RPM release, AgensGraph PG16 kernel single-package build
- Disable LLVM JIT on all EL targets for build stability
