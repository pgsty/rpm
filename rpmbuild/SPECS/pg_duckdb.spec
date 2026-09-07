%global _build_id_links none
# libduckdb is identical across PostgreSQL majors.  Keep the ELF build-id note,
# but suppress global symlinks that would collide across versioned packages.

%global pname pg_duckdb
%global sname pg_duckdb
%global pginstdir /usr/pgsql-%{pgmajorversion}
# Bound DuckDB's nested Ninja build independently of the PGXS bridge.
# Override with --define 'duckdb_core_jobs N' on builders with more memory.
%{!?duckdb_core_jobs:%global duckdb_core_jobs 2}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_duckdb 1.1.1 only supports PostgreSQL 14 through 18}
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.1
Release:	1PGSTY%{?dist}
Summary:	DuckDB-powered Postgres for high performance apps & analytics.
License:	MIT
URL:		https://github.com/duckdb/pg_duckdb
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_duckdb-1.1.1-install-order.patch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc gcc-c++ make cmake ninja-build python3 git
BuildRequires:	libcurl-devel lz4-devel openssl-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_duckdb is a Postgres extension that embeds DuckDB's columnar-vectorized analytics engine and features into Postgres.
We recommend using pg_duckdb to build high performance analytics and data-intensive applications.
pg_duckdb was developed in collaboration with our partners, Hydra and MotherDuck.

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
%set_build_flags
PG_CFLAGS="$CFLAGS"
PG_CXXFLAGS="$CXXFLAGS"
PG_LDFLAGS="$LDFLAGS"
DUCKDB_CFLAGS="$CFLAGS"
DUCKDB_CXXFLAGS="$CXXFLAGS"
DUCKDB_LDFLAGS="$LDFLAGS"
%if 0%{?rhel} >= 9
PG_CFLAGS="$(printf '%s\n' "$PG_CFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto /g')"
PG_CXXFLAGS="$(printf '%s\n' "$PG_CXXFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto /g')"
DUCKDB_CFLAGS="$(printf '%s\n' "$DUCKDB_CFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=1 /g')"
DUCKDB_CXXFLAGS="$(printf '%s\n' "$DUCKDB_CXXFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=1 /g')"
PG_LDFLAGS="$(printf '%s\n' "$PG_LDFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=2 /g')"
DUCKDB_LDFLAGS="$(printf '%s\n' "$DUCKDB_LDFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=1 /g')"
case " $PG_LDFLAGS " in *" -flto"*) ;; *) PG_LDFLAGS="$PG_LDFLAGS -flto=2" ;; esac
case " $DUCKDB_LDFLAGS " in *" -flto"*) ;; *) DUCKDB_LDFLAGS="$DUCKDB_LDFLAGS -flto=1" ;; esac
%endif
# The bundled DuckDB keeps function and line-table DWARF only (-g1); the PGXS
# bridge keeps the full distribution -g so the debuginfo package stays tractable.
DUCKDB_CFLAGS="$DUCKDB_CFLAGS -g1"
DUCKDB_CXXFLAGS="$DUCKDB_CXXFLAGS -g1"
DUCKDB_CMAKE_FLAGS="-DCMAKE_C_FLAGS:STRING=\"$DUCKDB_CFLAGS\" -DCMAKE_CXX_FLAGS:STRING=\"$DUCKDB_CXXFLAGS\" -DCMAKE_EXE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_SHARED_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_MODULE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\""
# DuckDB itself has no PostgreSQL-major input.  Reuse its build tree only
# inside this platform's RPM topdir, keyed by the complete source archive,
# compiler identity, distribution flags, and DuckDB build controls.  Copy the
# cache into the real source tree: DuckDB's CMake entry point is ../.. relative
# to this directory, so a symlink would resolve that path outside the source.
# PGXS bridge objects remain outside this tree and are rebuilt per PG major.
DUCKDB_CACHE_KEY="$(printf '%s\n' \
  "$(sha256sum %{SOURCE0})" \
  "$(${CXX:-c++} --version | head -1)" \
  "$DUCKDB_CFLAGS" "$DUCKDB_CXXFLAGS" "$DUCKDB_LDFLAGS" "$DUCKDB_CMAKE_FLAGS" \
  "${DUCKDB_BUILD:-Release}" "${DUCKDB_DISABLE_ASSERTIONS:-0}" | sha256sum | awk '{print $1}')"
DUCKDB_CACHE_DIR="%{_topdir}/.cache/pg_duckdb/$DUCKDB_CACHE_KEY"
if test -f "$DUCKDB_CACHE_DIR/.complete" && test -f "$DUCKDB_CACHE_DIR/release/src/libduckdb.so"; then
  mkdir -p third_party/duckdb/build
  cp -a "$DUCKDB_CACHE_DIR/." third_party/duckdb/build/
fi
PATH=%{pginstdir}/bin:$PATH \
  CMAKE_BUILD_PARALLEL_LEVEL=%{duckdb_core_jobs} \
  %{__make} -j%{duckdb_core_jobs} %{with_llvm_arg} \
  PG_CFLAGS="$PG_CFLAGS" PG_CXXFLAGS="$PG_CXXFLAGS" \
  LDFLAGS="$PG_LDFLAGS" \
  EXTRA_CMAKE_VARIABLES="$DUCKDB_CMAKE_FLAGS"
DUCKDB_CACHE_TMP="$DUCKDB_CACHE_DIR.tmp.$$"
rm -rf "$DUCKDB_CACHE_TMP"
mkdir -p "$DUCKDB_CACHE_TMP"
cp -a third_party/duckdb/build/. "$DUCKDB_CACHE_TMP/"
touch "$DUCKDB_CACHE_TMP/.complete"
rm -rf "$DUCKDB_CACHE_DIR"
mv "$DUCKDB_CACHE_TMP" "$DUCKDB_CACHE_DIR"

%install
%{__rm} -rf %{buildroot}
%set_build_flags
PG_CFLAGS="$CFLAGS"
PG_CXXFLAGS="$CXXFLAGS"
PG_LDFLAGS="$LDFLAGS"
DUCKDB_CFLAGS="$CFLAGS"
DUCKDB_CXXFLAGS="$CXXFLAGS"
DUCKDB_LDFLAGS="$LDFLAGS"
%if 0%{?rhel} >= 9
PG_CFLAGS="$(printf '%s\n' "$PG_CFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto /g')"
PG_CXXFLAGS="$(printf '%s\n' "$PG_CXXFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto /g')"
DUCKDB_CFLAGS="$(printf '%s\n' "$DUCKDB_CFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=1 /g')"
DUCKDB_CXXFLAGS="$(printf '%s\n' "$DUCKDB_CXXFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=1 /g')"
PG_LDFLAGS="$(printf '%s\n' "$PG_LDFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=2 /g')"
DUCKDB_LDFLAGS="$(printf '%s\n' "$DUCKDB_LDFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ -flto=1 /g')"
case " $PG_LDFLAGS " in *" -flto"*) ;; *) PG_LDFLAGS="$PG_LDFLAGS -flto=2" ;; esac
case " $DUCKDB_LDFLAGS " in *" -flto"*) ;; *) DUCKDB_LDFLAGS="$DUCKDB_LDFLAGS -flto=1" ;; esac
%endif
# The bundled DuckDB keeps function and line-table DWARF only (-g1); the PGXS
# bridge keeps the full distribution -g so the debuginfo package stays tractable.
DUCKDB_CFLAGS="$DUCKDB_CFLAGS -g1"
DUCKDB_CXXFLAGS="$DUCKDB_CXXFLAGS -g1"
DUCKDB_CMAKE_FLAGS="-DCMAKE_C_FLAGS:STRING=\"$DUCKDB_CFLAGS\" -DCMAKE_CXX_FLAGS:STRING=\"$DUCKDB_CXXFLAGS\" -DCMAKE_EXE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_SHARED_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_MODULE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\""
PATH=%{pginstdir}/bin:$PATH \
  CMAKE_BUILD_PARALLEL_LEVEL=%{duckdb_core_jobs} \
  %{__make} -j%{duckdb_core_jobs} %{with_llvm_arg} install DESTDIR=%{buildroot} \
  PG_CFLAGS="$PG_CFLAGS" PG_CXXFLAGS="$PG_CXXFLAGS" \
  LDFLAGS="$PG_LDFLAGS" \
  EXTRA_CMAKE_VARIABLES="$DUCKDB_CMAKE_FLAGS"

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/lib/libduckdb.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.1.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Declare the complete native and LLVM build dependency set
- Propagate build failures and package generated bitcode in the main package
- Preserve distribution debug and hardening flags while limiting DuckDB LTO
- Pass distribution debug flags through PGXS and DuckDB's nested CMake build
- Build the bundled DuckDB core with line-table debug information only (-g1)
- Reuse a source/compiler/flags-keyed DuckDB build tree across PG majors
- Limit the nested DuckDB Ninja build to two memory-safe jobs
- Limit each nested DuckDB LTO link to one worker for a global two-job bound
- Order the bundled DuckDB install after the PGXS library directory exists

* Sat Jul 11 2026 Vonng <rh@vonng.com> - 1.1.1-2PIGSTY
- Disable global build-id links so PostgreSQL-major packages can coexist
- Enforce the supported PostgreSQL 14 through 18 range

* Wed Dec 24 2025 Vonng <rh@vonng.com> - 1.1.1-1PIGSTY
* Tue Dec 16 2025 Vonng <rh@vonng.com> - 1.1.0-2PIGSTY
* Sat Nov 01 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- this is not published yet, but for pg_mooncake building 7daa8e53a
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.3.1-1PIGSTY
* Wed Dec 11 2024 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
* Thu Oct 24 2024 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- the first public release, used by Pigsty <https://pigsty.io>
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
