%global _build_id_links none
# libduckdb is identical across PostgreSQL majors.  Keep the ELF build-id note,
# but suppress global symlinks that would collide across versioned packages.

%global pname pg_duckdb
%global sname pg_duckdb
%global pginstdir /usr/pgsql-%{pgmajorversion}
# Bound DuckDB's nested Ninja build independently of the PGXS bridge.
# Override with --define 'duckdb_core_jobs N' on builders with more memory.
%{!?duckdb_core_jobs:%global duckdb_core_jobs 2}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:pg_duckdb is packaged for PostgreSQL 15 through 19}
%endif

%if 0%{?rhel} && 0%{?rhel} < 9
%{error:pg_duckdb requires Enterprise Linux 9 or newer}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg CLANG='$(LLVM_BINPATH)/clang'
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.2
Release:	1PGSTY%{?dist}
Summary:	DuckDB-powered Postgres for high performance apps & analytics.
License:	MIT
URL:		https://github.com/duckdb/pg_duckdb
Source0:	%{sname}-%{version}.tar.gz
%if 0%{?rhel} < 10
# httpfs needs libcurl >= 7.85; EL9 ships older headers.  This private
# static build input is not installed over the distribution libcurl.
Source1:	https://curl.se/download/curl-8.23.0.tar.gz
%endif
# Source archive includes DuckDB 8d78114e90a53823803660bf821f6073ac87da8c.
Patch0:		pg_duckdb-%{version}-source-archive.patch
Patch1:		pg_duckdb-%{version}-private-curl.patch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc gcc-c++ make cmake >= 3.18 ninja-build python3 git pkgconfig
BuildRequires:	libcurl-devel lz4-devel openssl-devel
%if 0%{?rhel} >= 10
BuildRequires:	patchelf
%endif
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Conflicts:	duckdb_fdw_%{pgmajorversion}

%description
pg_duckdb is a Postgres extension that embeds DuckDB's columnar-vectorized analytics engine and features into Postgres.
We recommend using pg_duckdb to build high performance analytics and data-intensive applications.
pg_duckdb was developed in collaboration with our partners, Hydra and MotherDuck.

%prep
%if 0%{?rhel} < 10
%autosetup -a 1 -p1 -n %{sname}-%{version}
%else
%autosetup -p1 -n %{sname}-%{version}
%endif

%if %llvm
# PGDG records the LLVM installation used for this PostgreSQL build in PGXS.
# Its major can differ from the distribution's current default.
%generate_buildrequires
pgxs=$(%{pginstdir}/bin/pg_config --pgxs)
llvm_bin=$(sed -n 's/^LLVM_BINPATH[[:space:]]*=[[:space:]]*//p' "$(dirname "$pgxs")/../Makefile.global")
test -n "$llvm_bin"
echo "$llvm_bin/clang"
echo "$llvm_bin/llvm-lto"
%endif

%build
%set_build_flags
export DUCKDB_COMMIT=8d78114e90a53823803660bf821f6073ac87da8c
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
# The bridge finds its bundled core in this PostgreSQL major's private lib
# directory. Use modern DT_RUNPATH instead of legacy DT_RPATH.
PG_LDFLAGS="$PG_LDFLAGS -Wl,--enable-new-dtags"
# Preserve full distribution DWARF for both the bridge and bundled DuckDB.
# The nested Release build keeps optimization while retaining these -g flags.
DUCKDB_CMAKE_FLAGS="-DCMAKE_C_FLAGS:STRING=\"$DUCKDB_CFLAGS\" -DCMAKE_CXX_FLAGS:STRING=\"$DUCKDB_CXXFLAGS\" -DCMAKE_EXE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_SHARED_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_MODULE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\""
CFLAGS="$DUCKDB_CFLAGS" LDFLAGS="$DUCKDB_LDFLAGS" \
  sh scripts/build-distribution-curl.sh "$PWD/curl-8.23.0" "$PWD/.pgsty-curl" %{duckdb_core_jobs}
if test -f .pgsty-curl/lib/libcurl.a; then
  DUCKDB_CMAKE_FLAGS="$DUCKDB_CMAKE_FLAGS -DCURL_ROOT=$PWD/.pgsty-curl -DCURL_USE_STATIC_LIBS=ON"
fi
# PGXS reuses the bundled shared library across majors. Keep generated C/C++
# sources for debugedit and debugsource, without copying intermediate objects.
DUCKDB_CACHE_KEY="$(printf '%s\n' \
  "$(sha256sum %{SOURCE0})" \
  "$(sha256sum %{PATCH0} %{PATCH1})" "$DUCKDB_COMMIT" \
%if 0%{?rhel} < 10
  "$(sha256sum %{SOURCE1})" \
%endif
  "$(pkg-config --modversion libcurl openssl)" \
  "$(${CXX:-c++} --version | head -1)" \
  "$DUCKDB_CFLAGS" "$DUCKDB_CXXFLAGS" "$DUCKDB_LDFLAGS" "$DUCKDB_CMAKE_FLAGS" \
  "${DUCKDB_BUILD:-Release}" "${DUCKDB_DISABLE_ASSERTIONS:-0}" | sha256sum | awk '{print $1}')"
DUCKDB_CACHE_DIR="%{_topdir}/.cache/pg_duckdb/$DUCKDB_CACHE_KEY"
duckdb_build_type=release
if test "${DUCKDB_BUILD:-Release}" = Debug; then duckdb_build_type=debug; fi
DUCKDB_CORE=third_party/duckdb/build/$duckdb_build_type/src/libduckdb.so
if test -s "$DUCKDB_CACHE_DIR/libduckdb.so" && test -s "$DUCKDB_CACHE_DIR/debug-sources.tar"; then
  tar -xf "$DUCKDB_CACHE_DIR/debug-sources.tar"
  mkdir -p "$(dirname "$DUCKDB_CORE")"
  cp --reflink=auto "$DUCKDB_CACHE_DIR/libduckdb.so" "$DUCKDB_CORE"
  touch "$DUCKDB_CORE"
fi
PATH=%{pginstdir}/bin:$PATH \
  CMAKE_BUILD_PARALLEL_LEVEL=%{duckdb_core_jobs} \
  %{__make} -j%{duckdb_core_jobs} %{with_llvm_arg} PG_DUCKDB_VERSION=v%{version} PG_MIN_VER=15 PG_MAX_VER=19 \
%if 0%{?pgmajorversion} >= 18
  PG_CPPFLAGS='-DPG_DUCKDB_VERSION=\"v%{version}\"' \
%endif
  PG_CFLAGS="$PG_CFLAGS" PG_CXXFLAGS="$PG_CXXFLAGS" \
  LDFLAGS="$PG_LDFLAGS" \
  EXTRA_CMAKE_VARIABLES="$DUCKDB_CMAKE_FLAGS"
if ! test -s "$DUCKDB_CACHE_DIR/libduckdb.so" || ! test -s "$DUCKDB_CACHE_DIR/debug-sources.tar"; then
  mkdir -p "$DUCKDB_CACHE_DIR"
  find "third_party/duckdb/build/$duckdb_build_type" -type f \( -name '*.c' -o -name '*.cc' -o -name '*.cpp' -o -name '*.cxx' \
    -o -name '*.h' -o -name '*.hh' -o -name '*.hpp' -o -name '*.inc' -o -name '*.S' \) -print0 > .duckdb-debug-sources
  tar -cf "$DUCKDB_CACHE_DIR/debug-sources.tar.$$" --null -T .duckdb-debug-sources
  mv -f "$DUCKDB_CACHE_DIR/debug-sources.tar.$$" "$DUCKDB_CACHE_DIR/debug-sources.tar"
  cp --reflink=auto "$DUCKDB_CORE" "$DUCKDB_CACHE_DIR/libduckdb.so.$$"
  mv -f "$DUCKDB_CACHE_DIR/libduckdb.so.$$" "$DUCKDB_CACHE_DIR/libduckdb.so"
fi

%install
%{__rm} -rf %{buildroot}
%set_build_flags
export DUCKDB_COMMIT=8d78114e90a53823803660bf821f6073ac87da8c
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
# Keep the bridge link flags identical when PGXS runs during installation.
PG_LDFLAGS="$PG_LDFLAGS -Wl,--enable-new-dtags"
# Preserve full distribution DWARF for both the bridge and bundled DuckDB.
# The nested Release build keeps optimization while retaining these -g flags.
DUCKDB_CMAKE_FLAGS="-DCMAKE_C_FLAGS:STRING=\"$DUCKDB_CFLAGS\" -DCMAKE_CXX_FLAGS:STRING=\"$DUCKDB_CXXFLAGS\" -DCMAKE_EXE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_SHARED_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\" -DCMAKE_MODULE_LINKER_FLAGS:STRING=\"$DUCKDB_LDFLAGS\""
if test -f .pgsty-curl/lib/libcurl.a; then
  DUCKDB_CMAKE_FLAGS="$DUCKDB_CMAKE_FLAGS -DCURL_ROOT=$PWD/.pgsty-curl -DCURL_USE_STATIC_LIBS=ON"
fi
PATH=%{pginstdir}/bin:$PATH \
  CMAKE_BUILD_PARALLEL_LEVEL=%{duckdb_core_jobs} \
  %{__make} -j%{duckdb_core_jobs} %{with_llvm_arg} install DESTDIR=%{buildroot} \
  PG_DUCKDB_VERSION=v%{version} PG_MIN_VER=15 PG_MAX_VER=19 \
%if 0%{?pgmajorversion} >= 18
  PG_CPPFLAGS='-DPG_DUCKDB_VERSION=\"v%{version}\"' \
%endif
  PG_CFLAGS="$PG_CFLAGS" PG_CXXFLAGS="$PG_CXXFLAGS" \
  LDFLAGS="$PG_LDFLAGS" \
  EXTRA_CMAKE_VARIABLES="$DUCKDB_CMAKE_FLAGS"

%if 0%{?rhel} >= 10
# EL10 validates RUNPATH as well as RPATH and rejects /usr/pgsql-N/lib.
# Resolve the bundled core beside the installed bridge in the same PG major.
patchelf --set-rpath '$ORIGIN' %{buildroot}%{pginstdir}/lib/%{pname}.so
%endif

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
* Tue Nov 24 2026 Ruohang Feng <rh@vonng.com> - 1.2.2-1PGSTY
- Package v1.2.2 with DuckDB 2.0.1 and the upstream 1.2.1 to 1.2.2 SQL update.
- Cache the shared core and generated debug sources across PostgreSQL majors.
- Require the Clang and llvm-lto binaries selected by PGXS.

* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 1.2.1-1PGSTY
- Package upstream 1.2.1 with its pinned DuckDB 2.0.1 source.
- Target PostgreSQL 15-19 and EL9+, with PG19 validated separately.
- Retire the upstreamed httpfs move fix and EL8-only compatibility code.
- Keep archive/install-order and private-curl changes in focused patches.
- Preserve full DWARF in the bridge, bundled DuckDB and private curl.
- Use the PGXS LLVM_BINPATH toolchain for core-compatible bitcode.

* Wed Nov 04 2026 Ruohang Feng <rh@vonng.com> - 1.2.0-1PGSTY
- Package upstream experimental 1.2.0 with its pinned DuckDB 2.0.0 source.
- Preserve the module version and DuckDB source identity without Git metadata.
- Apply the pinned httpfs source patch for GCC 8-11 unique_ptr conversion.
- Build private static curl 8.23.0 for httpfs when system libcurl is too old.
%if 0%{?rhel} == 8
- Select the parallel OpenSSL 3 headers and libraries on EL8.
- Probe httpfs C++ warning support before enabling it with GCC 8.
- Use GCC Toolset 15 for DuckDB 2.0 C++ library requirements on EL8.
%endif
- Include patches, dependency versions and source identity in the core cache key.
- Link the bridge with RUNPATH to its PostgreSQL-major-private DuckDB library.
%if 0%{?rhel} >= 10
- Use a relative private RUNPATH accepted by EL10 package validation.
%endif
- Retain PostgreSQL 14-18, LLVM, debug packaging and bounded core concurrency.

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
