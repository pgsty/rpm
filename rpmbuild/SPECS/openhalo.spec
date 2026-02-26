%global sname openhalo
%global openhaloversion 1.0
%global pgmajorversion 14
%global pgbaseinstdir	/usr/halo-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	%{openhaloversion}
Release:	beta1PIGSTY%{?dist}
Summary:	MySQL wire protocol support for PostgreSQL
License:	GPL-3.0
URL:		https://github.com/HaloTech-Co-Ltd/openHalo
Source0:	%{sname}-%{openhaloversion}.tar.gz

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel
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
Adding capability for PostgreSQL to work with applications written for MySQL but provides much more better performance than MySQL!

%prep
%setup -q -n %{sname}-%{openhaloversion}
patch -p1 < %{_specdir}/patches/%{sname}-%{openhaloversion}.patch

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
--with-libraries=/usr/lib \
--enable-nls \
--enable-dtrace

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin


%install
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin

%files
%doc README.md
%doc %{pgbaseinstdir}/doc/postgresql/extension/*.example
%license %{pgbaseinstdir}/LICENSE
%license %{pgbaseinstdir}/COPYRIGHT
%license %{pgbaseinstdir}/3party-legal-notices
%{pgbaseinstdir}/lib/*
%{pgbaseinstdir}/bin/*
%{pgbaseinstdir}/share/*
%{pgbaseinstdir}/include/*
%doc %{pgbaseinstdir}/doc/*

%pre
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Thu Feb 26 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.0-b1PIGSTY
* Wed Apr 02 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 14.10-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
