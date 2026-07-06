%global sname pgedge
%{!?pgmajorversion:%global pgmajorversion 18}
%if 0%{?pgmajorversion} == 18
%global pgversion 18.4
%elif 0%{?pgmajorversion} == 17
%global pgversion 17.10
%elif 0%{?pgmajorversion} == 16
%global pgversion 16.14
%elif 0%{?pgmajorversion} == 15
%global pgversion 15.18
%else
%{error:pgedge supports pgmajorversion 15, 16, 17, or 18}
%endif
%global spockversion 5.0.10
%global lolorversion 1.2.2
%global snowflakeversion 2.5.0
%global pgbaseinstdir /usr/pgedge-%{pgmajorversion}
# Private PostgreSQL ABI under a fork prefix, not a system libpq provider.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$

Name:           %{sname}-%{pgmajorversion}
Version:        %{pgversion}
Release:        1PIGSTY%{?dist}
Summary:        pgEdge PostgreSQL kernel with bundled replication extensions
License:        PostgreSQL
URL:            https://github.com/pgEdge
Source0:        postgresql-%{pgversion}.tar.gz
Source1:        spock-%{spockversion}.tar.gz
Source2:        lolor-%{lolorversion}.tar.gz
Source3:        snowflake-%{snowflakeversion}.tar.gz

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4
BuildRequires:  krb5-devel, libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel
BuildRequires:  jansson-devel, patchelf, pkgconfig
%if 0%{?rhel} >= 9
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
%else
BuildRequires:  perl-interpreter < 4:5.30
%endif
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2, tzdata
Requires(pre):  shadow-utils

%description
pgEdge patched PostgreSQL %{pgmajorversion} kernel package with bundled Spock,
LOLOR, and Snowflake extensions. This package installs PostgreSQL binaries,
libraries, headers, and extension payload under %{pgbaseinstdir}.

%prep
%setup -q -n postgresql-%{pgversion}

rm -rf .spock .lolor .snowflake .spock-src .lolor-src .snowflake-src
mkdir -p .spock-src .lolor-src .snowflake-src
tar -xzf %{SOURCE1} -C .spock-src
tar -xzf %{SOURCE2} -C .lolor-src
tar -xzf %{SOURCE3} -C .snowflake-src

spock_src=$(find .spock-src -mindepth 1 -maxdepth 1 -type d | head -n 1)
if [ -z "$spock_src" ]; then
  echo "cannot locate extracted spock source tree" >&2
  exit 1
fi
mv "$spock_src" .spock

lolor_src=$(find .lolor-src -mindepth 1 -maxdepth 1 -type d | head -n 1)
if [ -z "$lolor_src" ]; then
  echo "cannot locate extracted lolor source tree" >&2
  exit 1
fi
mv "$lolor_src" .lolor

snowflake_src=$(find .snowflake-src -mindepth 1 -maxdepth 1 -type d | head -n 1)
if [ -z "$snowflake_src" ]; then
  echo "cannot locate extracted snowflake source tree" >&2
  exit 1
fi
mv "$snowflake_src" .snowflake

if [ -d ".spock/patches/pg%{pgmajorversion}" ]; then
  patch_dir=".spock/patches/pg%{pgmajorversion}"
elif [ -d ".spock/patches/%{pgmajorversion}" ]; then
  patch_dir=".spock/patches/%{pgmajorversion}"
else
  echo "cannot locate spock patches for PG%{pgmajorversion}" >&2
  exit 1
fi

for patch_name in $(ls -1 "$patch_dir" | sort); do
  patch -p1 < "$patch_dir/$patch_name"
done

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
--with-extra-version=" (pgEdge %{spockversion})" \
--with-system-tzdata=/usr/share/zoneinfo \
--with-lz4 \
--with-zstd \
--with-uuid=e2fs \
--with-libxml \
--with-libxslt \
--with-icu \
--with-gssapi \
%if 0%{?rhel} >= 9
--with-perl \
%endif
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

rm -rf .pgedge-stage
MAKELEVEL=0 %{__make} DESTDIR="$PWD/.pgedge-stage" VERBOSE=1 %{?_smp_mflags} install-world-bin

cat > .pg_config_build <<'EOF'
#!/bin/sh
prefix="${PGEDGE_STAGE}%{pgbaseinstdir}"
case "$1" in
  --version) echo "PostgreSQL %{pgversion}" ;;
  --bindir) echo "${prefix}/bin" ;;
  --sharedir) echo "${prefix}/share/postgresql" ;;
  --sysconfdir) echo "${prefix}/etc/postgresql" ;;
  --libdir) echo "${prefix}/lib" ;;
  --pkglibdir) echo "${prefix}/lib/postgresql" ;;
  --includedir) echo "${prefix}/include" ;;
  --pkgincludedir) echo "${prefix}/include/postgresql" ;;
  --includedir-server) echo "${prefix}/include/postgresql/server" ;;
  --mandir) echo "${prefix}/share/man" ;;
  --docdir) echo "${prefix}/doc" ;;
  --localedir) echo "${prefix}/share/locale" ;;
  --pgxs) echo "${prefix}/lib/postgresql/pgxs/src/makefiles/pgxs.mk" ;;
  *) exec "${prefix}/bin/pg_config" "$@" ;;
esac
EOF
chmod +x .pg_config_build

for extdir in .spock .lolor .snowflake; do
  PGEDGE_STAGE="$PWD/.pgedge-stage" \
  PG_CONFIG="$PWD/.pg_config_build" \
  PATH="$PWD/.pgedge-stage%{pgbaseinstdir}/bin:$PATH" \
  USE_PGXS=1 \
  MAKELEVEL=0 %{__make} -C "$extdir" PG_CONFIG="$PWD/.pg_config_build" USE_PGXS=1 %{?_smp_mflags}
done

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin

cat > .pg_config_install <<'EOF'
#!/bin/sh
prefix="%{pgbaseinstdir}"
stage_prefix="${PGEDGE_STAGE}%{pgbaseinstdir}"
case "$1" in
  --version) echo "PostgreSQL %{pgversion}" ;;
  --bindir) echo "${prefix}/bin" ;;
  --sharedir) echo "${prefix}/share/postgresql" ;;
  --sysconfdir) echo "${prefix}/etc/postgresql" ;;
  --libdir) echo "${prefix}/lib" ;;
  --pkglibdir) echo "${prefix}/lib/postgresql" ;;
  --includedir) echo "${prefix}/include" ;;
  --pkgincludedir) echo "${prefix}/include/postgresql" ;;
  --includedir-server) echo "${prefix}/include/postgresql/server" ;;
  --mandir) echo "${prefix}/share/man" ;;
  --docdir) echo "${prefix}/doc" ;;
  --localedir) echo "${prefix}/share/locale" ;;
  --pgxs) echo "${stage_prefix}/lib/postgresql/pgxs/src/makefiles/pgxs.mk" ;;
  *) exec "${stage_prefix}/bin/pg_config" "$@" ;;
esac
EOF
chmod +x .pg_config_install

for extdir in .spock .lolor .snowflake; do
  PGEDGE_STAGE="$PWD/.pgedge-stage" \
  PG_CONFIG="$PWD/.pg_config_install" \
  PATH="$PWD/.pgedge-stage%{pgbaseinstdir}/bin:$PATH" \
  USE_PGXS=1 \
  MAKELEVEL=0 %{__make} -C "$extdir" PG_CONFIG="$PWD/.pg_config_install" USE_PGXS=1 install DESTDIR=%{buildroot}
done

for binary in \
  %{buildroot}%{pgbaseinstdir}/bin/spockctrl \
  %{buildroot}%{pgbaseinstdir}/lib/postgresql/spock.so \
  %{buildroot}%{pgbaseinstdir}/lib/postgresql/spock_output.so \
  %{buildroot}%{pgbaseinstdir}/lib/postgresql/lolor.so \
  %{buildroot}%{pgbaseinstdir}/lib/postgresql/snowflake.so; do
  [ -f "$binary" ] && patchelf --set-rpath "%{pgbaseinstdir}/lib" "$binary"
done

%files
%doc README*
%license COPYRIGHT
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
* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 18.4-1PIGSTY
- Bundle pgEdge PostgreSQL 18.4 with Spock 5.0.10, LOLOR 1.2.2, and Snowflake 2.5.0
- Rename package to pgedge-18 and obsolete the previous split pgEdge extension packages

* Fri May 01 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 18.3-1PIGSTY
- Build pgEdge PostgreSQL 18 kernel package with Spock 5.0.6 PG18 patchset

* Fri Feb 27 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.9-1PIGSTY
* Tue Feb 24 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.7-1PIGSTY
- Build pgEdge PostgreSQL kernel package and apply Spock PG17 patchset in prep stage
- EL8: drop perl-FindBin BuildRequires to avoid perl module stream conflict
- EL8: drop perl-ExtUtils-Embed BuildRequires to avoid perl module stream conflict
- EL8: use /usr/bin/perl BuildRequires to avoid perl module stream pull-up
