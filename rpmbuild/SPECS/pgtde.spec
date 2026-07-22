%global sname pgtde
%global pgmajorversion 18
%global pgversion 18.4
%global pgtdeversion 2.2.1
%global pgbaseinstdir /usr/pgtde-%{pgmajorversion}

%define debug_package %{nil}
%define _build_id_links none

# Private PostgreSQL ABI under a flavor prefix, not a system libpq provider.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$

Name:           %{sname}-%{pgmajorversion}
Version:        %{pgversion}
Release:        1PIGSTY%{?dist}
Summary:        Percona PostgreSQL kernel with transparent data encryption
License:        PostgreSQL
URL:            https://www.percona.com/postgresql/software/postgresql-distribution
Source0:        percona-postgresql-%{pgversion}.tar.gz
Source1:        percona-pg_tde%{pgmajorversion}-%{pgtdeversion}.tar.gz
Source2:        pgtde-pg-config

ExclusiveArch:  aarch64 x86_64

BuildRequires:  glibc-devel bison flex gettext chrpath gcc gcc-c++ make
BuildRequires:  readline-devel zlib-devel libselinux-devel libxml2-devel libxslt-devel
BuildRequires:  libuuid-devel lz4-devel libzstd-devel libicu-devel openldap-devel
BuildRequires:  pam-devel krb5-devel python3-devel tcl-devel systemtap-sdt-devel
BuildRequires:  openssl-devel systemd-devel libcurl-devel liburing-devel json-c-devel
BuildRequires:  meson ninja-build pkgconf-pkg-config
BuildRequires:  perl perl-ExtUtils-Embed perl-FindBin
Requires:       tzdata
Requires(pre):  shadow-utils

%description
Pigsty private-prefix build of Percona Server for PostgreSQL %{pgversion}
(Percona patch release 2) and pg_tde %{pgtdeversion}. The complete PostgreSQL
runtime, server, client, development files, PGXS, procedural languages, and
standard contrib modules are installed below %{pgbaseinstdir}.

The source inputs are pinned to Percona Server commit
be009d62926f7114a1a6af4f9775d36dc0f906a3 and pg_tde commit
53d79df6722428df3c24ad9a533e5c00ed9871da.

%package contrib
Summary:        Transparent data encryption extension for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       pg_tde = %{pgtdeversion}

%description contrib
The pg_tde %{pgtdeversion} extension and TDE-specific operational helpers for
the %{name} private PostgreSQL kernel. Modified PostgreSQL frontend utilities
are exposed under their canonical pg_* names by the main kernel package, with
the upstream pg_tde_* spellings retained as compatibility symlinks.

%prep
%setup -q -n percona-postgresql-%{pgversion}
%{__tar} -xzf %{SOURCE1}
%{__mv} percona-pg_tde%{pgmajorversion}-%{pgtdeversion} .pg_tde-src
%{__cp} -p %{SOURCE2} .pgtde-pg-config
%{__chmod} 0755 .pgtde-pg-config

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

# pg_tde is a Meson project that expects an installed PostgreSQL development
# tree. Stage the private kernel first and let the build-only pg_config wrapper
# report staged include/library paths. Meson then installs pg_tde into the same
# staging tree; the packaged pg_config still reports the final private prefix.
export PGTDE_STAGE="$(pwd)/.pgtde-stage"
%{__make} DESTDIR="$PGTDE_STAGE" %{?_smp_mflags} install-world-bin

meson setup .pgtde-build .pg_tde-src \
  --buildtype=release \
  -Dpg_config="$(pwd)/.pgtde-pg-config"
meson compile -C .pgtde-build
meson install -C .pgtde-build

%{__install} -D -m 0644 \
  .pg_tde-src/ci_scripts/perl/PostgreSQL/Test/TdeCluster.pm \
  "$PGTDE_STAGE%{pgbaseinstdir}/lib/postgresql/pgxs/src/test/perl/PostgreSQL/Test/TdeCluster.pm"

# Replace the staged build path in pg_tde frontend RPATHs with the final
# private library directory. Core PostgreSQL binaries already carry this RPATH
# because the kernel itself is configured with --enable-rpath.
find "$PGTDE_STAGE%{pgbaseinstdir}" -type f \
  \( -name 'pg_tde*' -o -name 'pg_tde.so' \) -perm /111 -print0 | \
  xargs -0 -r -n 1 chrpath --replace %{pgbaseinstdir}/lib 2>/dev/null || :

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}
%{__cp} -a .pgtde-stage/usr %{buildroot}/

# A private PostgreSQL flavor must make its TDE-aware utilities the safe
# defaults. Keep the Percona names as symlinks for upstream documentation and
# compatibility with existing Patroni bin_name mappings.
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

%check
test "$(.pgtde-stage%{pgbaseinstdir}/bin/pg_config --version)" = \
  "PostgreSQL %{pgversion} - Percona Server for PostgreSQL 18.4.2"
test -f %{buildroot}%{pgbaseinstdir}/lib/postgresql/pg_tde.so
test -f %{buildroot}%{pgbaseinstdir}/share/postgresql/extension/pg_tde.control
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

%files
%doc README* HISTORY
%license COPYRIGHT
%{pgbaseinstdir}
%exclude %{pgbaseinstdir}/bin/pg_tde_change_key_provider
%exclude %{pgbaseinstdir}/bin/pg_tde_archive_decrypt
%exclude %{pgbaseinstdir}/bin/pg_tde_restore_encrypt
%exclude %{pgbaseinstdir}/lib/postgresql/pg_tde.so
%exclude %{pgbaseinstdir}/share/postgresql/extension/pg_tde.control
%exclude %{pgbaseinstdir}/share/postgresql/extension/pg_tde*.sql
%exclude %{pgbaseinstdir}/lib/postgresql/pgxs/src/test/perl/PostgreSQL/Test/TdeCluster.pm

%files contrib
%doc .pg_tde-src/README.md
%license .pg_tde-src/COPYRIGHT
%{pgbaseinstdir}/bin/pg_tde_change_key_provider
%{pgbaseinstdir}/bin/pg_tde_archive_decrypt
%{pgbaseinstdir}/bin/pg_tde_restore_encrypt
%{pgbaseinstdir}/lib/postgresql/pg_tde.so
%{pgbaseinstdir}/share/postgresql/extension/pg_tde.control
%{pgbaseinstdir}/share/postgresql/extension/pg_tde*.sql
%{pgbaseinstdir}/lib/postgresql/pgxs/src/test/perl/PostgreSQL/Test/TdeCluster.pm

%pre
getent group postgres >/dev/null 2>&1 || groupadd -g 26 -r postgres >/dev/null 2>&1 || groupadd -r postgres >/dev/null 2>&1 || :
getent passwd postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" postgres >/dev/null 2>&1 || :

%changelog
* Wed Jul 22 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 18.4-1PIGSTY
- Add the Percona PostgreSQL 18.4.2 kernel and pg_tde 2.2.1 under /usr/pgtde-18
- Promote TDE-aware frontend tools to canonical PostgreSQL command names
