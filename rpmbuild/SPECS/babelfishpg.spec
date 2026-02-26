%global sname babelfishpg
%global pgmajorversion 17
%global pgsourceversion 17.8-5.5.0
%global pgbaseinstdir /usr/babelfish-%{pgmajorversion}
%global pgsysinstdir /usr/pgsql-%{pgmajorversion}

Name:           %{sname}_%{pgmajorversion}
Version:        17.8
Release:        1PIGSTY%{?dist}
Summary:        Babelfish PostgreSQL kernel (PG17)
License:        PostgreSQL
URL:            https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish
Source0:        %{sname}-%{pgsourceversion}.tar.gz

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4, clang, llvm, clang-devel, llvm-devel
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2
Requires(pre):  shadow-utils

%description
Babelfish patched PostgreSQL 17 kernel package.
This package installs PostgreSQL binaries and libraries under %{pgbaseinstdir}.

%prep
%setup -q -n %{sname}-%{pgsourceversion}
cp -a postgresql_modified_for_babelfish/. .

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
--without-llvm \
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
%license LICENSE.PostgreSQL
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
* Thu Feb 19 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.8-1PIGSTY
- Split Babelfish build chain: kernel package only (extensions moved out)
