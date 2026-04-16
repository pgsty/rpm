%global sname oriolepg
%global pgmajorversion 17
%global pgbaseinstdir	/usr/oriole-%{pgmajorversion}
%global orioledb_patchset 18
%global upstream_pgver 17.7
%global srcdir postgres-patches17_%{orioledb_patchset}

Name:		%{sname}_%{pgmajorversion}
Version:	17.%{orioledb_patchset}
Release:	1PIGSTY%{?dist}
Summary:	Modern cloud-native storage engine for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/orioledb/orioledb
Source0:	%{srcdir}.tar.gz
# upstream codeload tarball from https://github.com/orioledb/postgres/tree/patches17_18

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
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
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2
Requires(pre):  shadow-utils

%description
This is the patched PostgreSQL %{pgmajorversion} kernel package for OrioleDB extension
based on PostgreSQL %{upstream_pgver} and upstream OrioleDB patchset %{orioledb_patchset}.
OrioleDB is a new storage engine for PostgreSQL, bringing a modern approach to database capacity, capabilities and performance to the world's most-loved database platform.
OrioleDB consists of an extension, building on the innovative table access method framework and other standard Postgres extension interfaces.
By extending and enhancing the current table access methods, OrioleDB opens the door to a future of more powerful storage models that are optimized for cloud and modern hardware architectures.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{_specdir}/patches/oriolepg-postgresql-branding.patch

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
--with-extra-version=" (OrioleDB 1.7-beta15)" \
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

# Source tarball build has no git metadata, force patchset for PGXS consumers.
sed -ri 's|^ORIOLEDB_PATCHSET_VERSION =.*|ORIOLEDB_PATCHSET_VERSION = %{orioledb_patchset}|' src/Makefile.global

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin


%install
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin

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
* Thu Apr 16 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.18-1PIGSTY
- Rebase the PG17 kernel package to upstream patches17_18 (PostgreSQL 17.7)
- Apply the OrioleDB branding change as a packaging patch instead of repacking the source tarball

* Thu Feb 26 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.16-1PIGSTY
* Thu Jul 24 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 17.11-1PIGSTY
* Tue May 27 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 17.9-1PIGSTY
* Sat Apr 05 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 17.0-6PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
