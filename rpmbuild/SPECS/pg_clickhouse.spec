%define debug_package %{nil}
%global pname pg_clickhouse
%global sname pg_clickhouse
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.3
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension to query ClickHouse databases
License:	Apache-2.0
URL:		https://github.com/ClickHouse/pg_clickhouse
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/ClickHouse/pg_clickhouse/archive/refs/tags/v0.1.3.tar.gz
#           Supported: PostgreSQL 13, 14, 15, 16, 17, 18

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	automake
BuildRequires:	openssl-devel
BuildRequires:	libcurl-devel
BuildRequires:	libuuid-devel

Requires:	postgresql%{pgmajorversion}-server
Requires:	openssl libcurl libuuid

%description
pg_clickhouse is a PostgreSQL extension that runs analytics queries on
ClickHouse right from PostgreSQL without rewriting any SQL. It enables
seamless querying of ClickHouse databases directly from PostgreSQL.

Features:
- Query Pushdown: Automatically optimizes queries by pushing them to ClickHouse
- TPC-H Performance: Achieves substantial speedups on analytical workloads
- No SQL Rewrites: Use standard PostgreSQL syntax for ClickHouse queries
- Supports PostgreSQL 13+ and ClickHouse v23+

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

# Skip git submodule command since vendor/clickhouse-cpp is already included in tarball
sed -i 's/git submodule update --init/@echo "Skipping submodule (included in tarball)"/' Makefile

%build
# Makefile will auto-build vendor/clickhouse-cpp via cmake
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%{pginstdir}/doc/extension/%{pname}.md
%exclude %{pginstdir}/doc/extension/tutorial.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Sun Jan 25 2026 Vonng <rh@vonng.com> - 0.1.3-1PIGSTY
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 0.1.2-1PIGSTY
* Mon Dec 16 2025 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
