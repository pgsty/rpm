%global _build_id_links none
# libduckdb is identical across PostgreSQL majors.  Keep the ELF build-id note,
# but suppress global symlinks that would collide across versioned packages.

%global pname pg_duckdb
%global sname pg_duckdb
%global pginstdir /usr/pgsql-%{pgmajorversion}

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
%if 0%{?rhel} >= 9
CFLAGS="$(printf '%s\n' "$CFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ /g; s/(^|[[:space:]])-ffat-lto-objects([[:space:]]|$)/ /g')"
CXXFLAGS="$(printf '%s\n' "$CXXFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ /g; s/(^|[[:space:]])-ffat-lto-objects([[:space:]]|$)/ /g')"
%endif
PATH=%{pginstdir}/bin:$PATH CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" \
  %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%set_build_flags
%if 0%{?rhel} >= 9
CFLAGS="$(printf '%s\n' "$CFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ /g; s/(^|[[:space:]])-ffat-lto-objects([[:space:]]|$)/ /g')"
CXXFLAGS="$(printf '%s\n' "$CXXFLAGS" | sed -E 's/(^|[[:space:]])-flto(=[^[:space:]]*)?([[:space:]]|$)/ /g; s/(^|[[:space:]])-ffat-lto-objects([[:space:]]|$)/ /g')"
%endif
PATH=%{pginstdir}/bin:$PATH CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" \
  %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

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
- Propagate build failures and package the generated llvmjit payload
- Preserve distribution debug and hardening flags while limiting DuckDB LTO
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
