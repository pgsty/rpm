%global pname pg_clickhouse
%global sname pg_clickhouse
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch x86_64
 %if 0%{?rhel} && 0%{?rhel} == 9
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.10.0
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension to query ClickHouse databases
License:	Apache-2.0
URL:		https://github.com/ClickHouse/pg_clickhouse
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_clickhouse-0.10.0.patch
#           normalized from https://api.pgxn.org/dist/pg_clickhouse/0.10.0/pg_clickhouse-0.10.0.zip
#           vendor/pg-clickhouse-c and clickhouse-c are included in the PGXN source bundle
#           Supported: PostgreSQL 14, 15, 16, 17, 18

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
BuildRequires:	openssl-devel
BuildRequires:	libcurl-devel
BuildRequires:	libuuid-devel
BuildRequires:	lz4-devel
BuildRequires:	libzstd-devel

%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	openssl libcurl libuuid lz4-libs libzstd

%description
pg_clickhouse is a PostgreSQL extension that runs analytics queries on
ClickHouse right from PostgreSQL without rewriting any SQL. It enables
seamless querying of ClickHouse databases directly from PostgreSQL.

Features:
- Query Pushdown: Automatically optimizes queries by pushing them to ClickHouse
- TPC-H Performance: Achieves substantial speedups on analytical workloads
- No SQL Rewrites: Use standard PostgreSQL syntax for ClickHouse queries
- Supports PostgreSQL 14-18 in Pigsty builds and ClickHouse v23+

%prep
%autosetup -p1 -n %{sname}-%{version}

# Skip git submodule command since the recursive vendor tree is included.
sed -i 's/git submodule update --init/@echo "Skipping submodule (included in tarball)"/' Makefile
# PostgreSQL packages on EL9 x86_64 inject -flto=auto through pg_config,
# which trips gcc's LTO jobserver path for this PGXS build.
%ifarch x86_64
%if 0%{?rhel} == 9
sed -i '/^PG_CFLAGS =/a PG_CFLAGS += -fno-lto' Makefile
%endif
%endif
%build
# Makefile uses the vendored clickhouse-c headers from the PGXN bundle
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE.md
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%{pginstdir}/doc/extension/%{pname}.md
%exclude %{pginstdir}/doc/extension/tutorial.md

%if %llvm
   %{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.10.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Aug 12 2026 Vonng <rh@vonng.com> - 0.10.0-1PIGSTY
- Update to upstream PGXN 0.10.0 with the recursive vendored C client
- Replace the obsolete C++ build dependency with the upstream C toolchain
- Mark the endpoint pointer volatile across PG_TRY for GCC 16 builds

* Thu Jun 18 2026 Vonng <rh@vonng.com> - 0.3.2-1PIGSTY
- Update to upstream PGXN 0.3.2 using the normalized source tarball
- Disable JIT subpackages on EL9 x86_64 to avoid llvm-lto install crashes
- Disable PGXS gcc LTO on EL9 x86_64 to avoid link-time jobserver failures

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.3.1-1PIGSTY
- Update to upstream PGXN 0.3.1 using the normalized source tarball

* Thu May 14 2026 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Update to upstream PGXN 0.3.0 using the normalized source tarball with the vendored clickhouse-cpp tree

* Thu Apr 16 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Update to upstream 0.2.0 using the normalized PGXN source tarball with the vendored clickhouse-cpp tree
- Drop the local libcurl compatibility patch because upstream now defines CURL_WRITEFUNC_ERROR in both HTTP drivers

* Wed Apr 08 2026 Vonng <rh@vonng.com> - 0.1.10-1PIGSTY
- https://github.com/ClickHouse/pg_clickhouse/releases/tag/v0.1.10
- Repacked recursive git clone with vendored clickhouse-cpp submodule

* Mon Apr 06 2026 Vonng <rh@vonng.com> - 0.1.6-1PIGSTY
- https://github.com/ClickHouse/pg_clickhouse/releases/tag/v0.1.6
* Sat Mar 21 2026 Vonng <rh@vonng.com> - 0.1.5-1PIGSTY
* Wed Feb 18 2026 Vonng <rh@vonng.com> - 0.1.4-1PIGSTY
* Sun Jan 25 2026 Vonng <rh@vonng.com> - 0.1.3-1PIGSTY
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 0.1.2-1PIGSTY
* Tue Dec 16 2025 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
