%global sname babelfish
%{!?pgmajorversion:%global pgmajorversion 17}
%{!?pgversion:%global pgversion 17.7}
%{!?bbfversion:%global bbfversion 5.4.0}
%global sourceversion %{pgversion}-%{bbfversion}
%global pginstdir /usr/babelfish-%{pgmajorversion}
# Private PostgreSQL ABI under a fork prefix, not a system libpq provider.
%global __provides_exclude_from ^%{pginstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$
%global buildstage %{_builddir}/%{name}-%{version}-stage
%global bbf_prefix_map -ffile-prefix-map=%{buildstage}=%{pginstdir} -ffile-prefix-map=%{_builddir}/%{sname}-%{pgmajorversion}-%{sourceversion}=.
%define debug_package %{nil}

Name:           %{sname}-%{pgmajorversion}
Version:        %{bbfversion}
Release:        1PIGSTY%{?dist}
Summary:        Babelfish PostgreSQL kernel and core extensions for PG %{pgmajorversion}
License:        PostgreSQL
URL:            https://github.com/babelfish-for-postgresql
Source0:        %{sname}-%{pgmajorversion}-%{sourceversion}.tar.gz

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4, clang, llvm, clang-devel, llvm-devel
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
BuildRequires:  antlr4-runtime413-devel >= 4.13.2
BuildRequires:  bison, flex, cmake
%if 0%{?rhel} >= 10
BuildRequires:  java-21-openjdk-headless
%else
BuildRequires:  java-17-openjdk-headless
%endif
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2, tzdata
Requires:       antlr4-runtime413 >= 4.13.2
Requires(pre):  shadow-utils

%description
Babelfish patched PostgreSQL %{pgmajorversion} kernel bundled with the core
Babelfish extension payload:
- babelfishpg_money
- babelfishpg_common
- babelfishpg_tsql
- babelfishpg_tds

The package installs PostgreSQL binaries, libraries, headers, shared files,
and Babelfish extensions under %{pginstdir}.

%prep
%setup -q -n %{sname}-%{pgmajorversion}-%{sourceversion}
rm -rf buildsrc
mkdir -p buildsrc/contrib
cp -a postgresql_modified_for_babelfish/. buildsrc/
for ext in babelfishpg_money babelfishpg_common babelfishpg_tsql babelfishpg_tds; do
  cp -a babelfish_extensions/contrib/$ext buildsrc/contrib/
done
sed -i -e 's/Oid[[:space:]]*function_id;/Oid			function_id = InvalidOid;/' \
  buildsrc/contrib/babelfishpg_tsql/src/procedures.c

%build
cd buildsrc
CFLAGS="${CFLAGS:-%optflags} %{bbf_prefix_map}"
CFLAGS=`echo $CFLAGS | xargs -n 1 | grep -v ffast-math | xargs -n 100`
%if 0%{?pgmajorversion} >= 18
CFLAGS="$CFLAGS -Wno-error=missing-variable-declarations -DHAVE_OPENSSL_INIT_SSL -DHAVE_BIO_METH_NEW"
%endif
CXXFLAGS="${CXXFLAGS:-%optflags} %{bbf_prefix_map}"
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
export CFLAGS CXXFLAGS

./configure --enable-rpath \
--prefix=%{pginstdir} \
--includedir=%{pginstdir}/include \
--mandir=%{pginstdir}/share/man \
--datadir=%{pginstdir}/share \
--libdir=%{pginstdir}/lib \
--docdir=%{pginstdir}/doc \
--htmldir=%{pginstdir}/doc/html \
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

rm -rf %{buildstage}
MAKELEVEL=0 %{__make} DESTDIR=%{buildstage} install-world-bin

cat > bbf-pg_config <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
real="%{buildstage}%{pginstdir}/bin/pg_config"
stage="%{buildstage}"
prefix="%{pginstdir}"

if [[ $# -ne 1 ]]; then
  exec "${real}" "$@"
fi

case "$1" in
  --bindir|--docdir|--htmldir|--includedir|--includedir-server|--sharedir|--sysconfdir|--pgxs)
    out="$("${real}" "$1")"
    case "${out}" in
      "${prefix}"*) printf '%s%s\n' "${stage}" "${out}" ;;
      *) printf '%s\n' "${out}" ;;
    esac
    ;;
  --libdir|--pkglibdir)
    out="$("${real}" "$1")"
    case "${out}" in
      "${stage}${prefix}"*) printf '%s%s\n' "${prefix}" "${out#"${stage}${prefix}"}" ;;
      *) printf '%s\n' "${out}" ;;
    esac
    ;;
  *) exec "${real}" "$1" ;;
esac
EOF
chmod +x bbf-pg_config

export PATH=$(pwd):%{buildstage}%{pginstdir}/bin:$PATH
export PG_CONFIG=$(pwd)/bbf-pg_config
export PG_SRC=$(pwd)
export ANTLR4_JAVA_BIN=/usr/bin/java
export ANTLR4_RUNTIME_LIB=-lantlr4-runtime
export ANTLR4_RUNTIME_INCLUDE_DIR=%{_includedir}/antlr4-runtime
export ANTLR4_RUNTIME_LIB_DIR=%{_libdir}
export cmake=/usr/bin/cmake
export PG_CXXFLAGS="${PG_CXXFLAGS:-} %{bbf_prefix_map} -Wno-error=overloaded-virtual"
export PG_CFLAGS="${PG_CFLAGS:-} %{bbf_prefix_map} -Wno-error=date-time -Wno-error=stringop-overflow"
export CFLAGS="$CFLAGS -Wno-error=date-time -Wno-error=stringop-overflow"

sed -ri 's#SET \(MYDIR /usr/local/include/antlr4-runtime/\)#SET (MYDIR %{_includedir}/antlr4-runtime/)#' \
  contrib/babelfishpg_tsql/antlr/CMakeLists.txt
sed -ri 's#^export ANTLR4_RUNTIME_INCLUDE_DIR=.*#export ANTLR4_RUNTIME_INCLUDE_DIR=%{_includedir}/antlr4-runtime#' \
  contrib/babelfishpg_tsql/Makefile
sed -ri 's#^export ANTLR4_RUNTIME_LIB_DIR=.*#export ANTLR4_RUNTIME_LIB_DIR=%{_libdir}#' \
  contrib/babelfishpg_tsql/Makefile

# Replace the fault injection test object with a runtime stub. PGXS auto-discovers
# all C files here, and PG18 links the test object into the main TDS module.
cat > contrib/babelfishpg_tds/src/backend/fault_injection/fault_injection_stub.c <<'EOF'
#include "postgres.h"
#include "src/include/faultinjection.h"

static void
noop_fault(void *arg, int *num_occurrences)
{
	(void) arg;
	if (num_occurrences != NULL && *num_occurrences > 0)
		(*num_occurrences)--;
}

TEST_TYPE_LIST =
{
	{ TestType, "Test", NIL },
	{ ParseHeaderType, "TDS request header", NIL },
	{ PreParsingType, "TDS pre-parsing", NIL },
	{ ParseRpcType, "TDS RPC Parsing", NIL },
	{ PostParsingType, "TDS post-parsing", NIL },
	{ InvalidType, "", NIL }
};

TEST_LIST =
{
	{ "noop_fault", TestType, 0, &noop_fault },
	{ "", InvalidType, 0, NULL }
};
EOF
if [ -f contrib/babelfishpg_tds/src/backend/fault_injection/fault_injection_tests.c ]; then
  mv contrib/babelfishpg_tds/src/backend/fault_injection/fault_injection_tests.c \
     contrib/babelfishpg_tds/src/backend/fault_injection/fault_injection_tests.c.disabled
fi

%{__make} -C contrib/babelfishpg_money %{?_smp_mflags} with_llvm=no
%{__make} -C contrib/babelfishpg_common %{?_smp_mflags} with_llvm=no
%{__make} -C contrib/babelfishpg_tds %{?_smp_mflags} with_llvm=no
%{__make} -C contrib/babelfishpg_tsql antlr/libantlr_tsql.a cmake=/usr/bin/cmake with_llvm=no
if [ ! -d contrib/babelfishpg_tsql/antlr/antlr4cpp_generated_src/TSqlLexer ]; then
  mkdir -p contrib/babelfishpg_tsql/antlr/antlr4cpp_generated_src
  cp -a contrib/babelfishpg_tsql/antlr/CMakeFiles/antlr_tsql.dir/antlr4cpp_generated_src/TSqlLexer \
        contrib/babelfishpg_tsql/antlr/CMakeFiles/antlr_tsql.dir/antlr4cpp_generated_src/TSqlParser \
        contrib/babelfishpg_tsql/antlr/antlr4cpp_generated_src/
fi
%{__make} -C contrib/babelfishpg_tsql cmake=/usr/bin/cmake with_llvm=no

%install
%{__rm} -rf %{buildroot}
cd buildsrc
MAKELEVEL=0 %{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin

export PATH=$(pwd):%{buildstage}%{pginstdir}/bin:$PATH
export PG_CONFIG=$(pwd)/bbf-pg_config
export PG_SRC=$(pwd)
export ANTLR4_JAVA_BIN=/usr/bin/java
export ANTLR4_RUNTIME_LIB=-lantlr4-runtime
export ANTLR4_RUNTIME_INCLUDE_DIR=%{_includedir}/antlr4-runtime
export ANTLR4_RUNTIME_LIB_DIR=%{_libdir}
export cmake=/usr/bin/cmake

%{__make} -C contrib/babelfishpg_money install with_llvm=no DESTDIR=%{buildroot} \
  pkglibdir=%{pginstdir}/lib/postgresql datadir=%{pginstdir}/share/postgresql
%{__make} -C contrib/babelfishpg_common install with_llvm=no DESTDIR=%{buildroot} \
  pkglibdir=%{pginstdir}/lib/postgresql datadir=%{pginstdir}/share/postgresql
%{__make} -C contrib/babelfishpg_tsql install with_llvm=no DESTDIR=%{buildroot} \
  pkglibdir=%{pginstdir}/lib/postgresql datadir=%{pginstdir}/share/postgresql
%{__make} -C contrib/babelfishpg_tds install with_llvm=no DESTDIR=%{buildroot} \
  pkglibdir=%{pginstdir}/lib/postgresql datadir=%{pginstdir}/share/postgresql

%files
%doc buildsrc/README.md
%license buildsrc/COPYRIGHT
%license buildsrc/LICENSE.PostgreSQL
%{pginstdir}/lib/*
%{pginstdir}/bin/*
%{pginstdir}/share/*
%{pginstdir}/include/*
%doc %{pginstdir}/doc/*

%pre
getent group postgres >/dev/null 2>&1 || groupadd -g 26 -r postgres >/dev/null 2>&1 || groupadd -r postgres >/dev/null 2>&1 || :
getent passwd postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 5.4.0-1PIGSTY
- Bundle Babelfish PG 17.7 kernel and 5.4.0 core extensions into babelfish-17
