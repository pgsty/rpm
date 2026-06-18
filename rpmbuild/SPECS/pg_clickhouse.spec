%define debug_package %{nil}
%global pname pg_clickhouse
%global sname pg_clickhouse
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

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

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.2
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension to query ClickHouse databases
License:	Apache-2.0
URL:		https://github.com/ClickHouse/pg_clickhouse
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_clickhouse/0.3.2/pg_clickhouse-0.3.2.zip
#           vendor/clickhouse-c is already included in the PGXN source bundle
#           Supported: PostgreSQL 14, 15, 16, 17, 18

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++
BuildRequires:	openssl-devel
BuildRequires:	libcurl-devel
BuildRequires:	libuuid-devel
BuildRequires:	lz4-devel
BuildRequires:	libzstd-devel

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

# Skip git submodule command since vendor/clickhouse-c is already included in tarball
sed -i 's/git submodule update --init/@echo "Skipping submodule (included in tarball)"/' Makefile
# PostgreSQL packages on EL9 x86_64 inject -flto=auto through pg_config,
# which trips gcc's LTO jobserver path for this PGXS build.
%ifarch x86_64
%if 0%{?rhel} == 9
sed -i '/^PG_CFLAGS =/a PG_CFLAGS += -fno-lto' Makefile
%endif
%endif
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}-openssl-init.patch

%build
# Makefile uses the vendored clickhouse-c headers from the PGXN bundle
%if %llvm
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}
%else
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} with_llvm=no
%endif

%install
%{__rm} -rf %{buildroot}
%if %llvm
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}
%else
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} with_llvm=no
%endif

%files
%license LICENSE.md
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
