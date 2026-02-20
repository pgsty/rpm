%global sname babelfish
%global pgmajorversion 17
%global pgversion 17.8
%global bbfversion 5.5.0
%global sourceversion %{pgversion}-%{bbfversion}
%global pginstdir /usr/babelfish-%{pgmajorversion}

Name:           %{sname}_%{pgmajorversion}
Version:        %{bbfversion}
Release:        1PIGSTY%{?dist}
Summary:        Babelfish core extensions for PostgreSQL %{pgmajorversion}
License:        PostgreSQL
URL:            https://github.com/babelfish-for-postgresql/babelfish_extensions
Source0:        babelfishpg-%{sourceversion}.tar.gz

BuildRequires:  babelfishpg_%{pgmajorversion} >= %{pgversion}
BuildRequires:  antlr4-runtime413-devel >= 4.13.2
BuildRequires:  bison, flex, cmake
%if 0%{?rhel} >= 10
BuildRequires:  java-21-openjdk-headless
%else
BuildRequires:  java-17-openjdk-headless
%endif
BuildRequires:  openssl-devel, libicu-devel, perl
Requires:       babelfishpg_%{pgmajorversion} >= %{pgversion}
Requires:       antlr4-runtime413 >= 4.13.2

%description
Core Babelfish extension bundle for Babelfish PG %{pgmajorversion}:
- babelfishpg_money
- babelfishpg_common
- babelfishpg_tsql
- babelfishpg_tds

%prep
%setup -q -n babelfishpg-%{sourceversion}
rm -rf buildsrc
mkdir -p buildsrc/contrib
cp -a postgresql_modified_for_babelfish/. buildsrc/
for ext in babelfishpg_money babelfishpg_common babelfishpg_tsql babelfishpg_tds; do
  cp -a babelfish_extensions/contrib/$ext buildsrc/contrib/
done

%build
cd buildsrc
export PATH=%{pginstdir}/bin:$PATH
export PG_CONFIG=%{pginstdir}/bin/pg_config
export PG_SRC=$(pwd)
export ANTLR4_JAVA_BIN=/usr/bin/java
export ANTLR4_RUNTIME_LIB=-lantlr4-runtime
export ANTLR4_RUNTIME_INCLUDE_DIR=%{_includedir}/antlr4-runtime
export ANTLR4_RUNTIME_LIB_DIR=%{_libdir}
export cmake=/usr/bin/cmake
export PG_CXXFLAGS="-Wno-error=overloaded-virtual"
export PG_CFLAGS="$PG_CFLAGS -Wno-error=date-time -Wno-error=stringop-overflow"
export CFLAGS="$CFLAGS -Wno-error=date-time -Wno-error=stringop-overflow"

sed -ri 's#SET \(MYDIR /usr/local/include/antlr4-runtime/\)#SET (MYDIR %{_includedir}/antlr4-runtime/)#' \
  contrib/babelfishpg_tsql/antlr/CMakeLists.txt
sed -ri 's#^export ANTLR4_RUNTIME_INCLUDE_DIR=.*#export ANTLR4_RUNTIME_INCLUDE_DIR=%{_includedir}/antlr4-runtime#' \
  contrib/babelfishpg_tsql/Makefile
sed -ri 's#^export ANTLR4_RUNTIME_LIB_DIR=.*#export ANTLR4_RUNTIME_LIB_DIR=%{_libdir}#' \
  contrib/babelfishpg_tsql/Makefile

# fault_injection_tests.c defines required symbols but is excluded due -Werror
# issues on PG17. This is NOT EL8-only: EL8/EL9/EL10 can all hit unresolved
# symbols at runtime (e.g. FaultInjectionTypes). Keep this stub cross-EL until
# upstream fault injection objects can be built safely again.
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
export PATH=%{pginstdir}/bin:$PATH
export PG_CONFIG=%{pginstdir}/bin/pg_config
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
%{pginstdir}/lib/postgresql/babelfishpg_*.so
%{pginstdir}/share/postgresql/extension/*.control
%{pginstdir}/share/postgresql/extension/*.sql

%changelog
* Thu Feb 19 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 5.5.0-1PIGSTY
- Build Babelfish extensions as standalone package against babelfishpg and antlr4-runtime413
