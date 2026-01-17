%define debug_package %{nil}
%global _unique_build_ids 1
# libduckdb has same build-id which require unique build id to avoid conflict

%global pname pg_duckdb
%global sname pg_duckdb
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
Version:	1.1.1
Release:	1PIGSTY%{?dist}
Summary:	DuckDB-powered Postgres for high performance apps & analytics.
License:	MIT
URL:		https://github.com/duckdb/pg_duckdb
Source0:	%{sname}-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 libcurl-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_duckdb is a Postgres extension that embeds DuckDB's columnar-vectorized analytics engine and features into Postgres.
We recommend using pg_duckdb to build high performance analytics and data-intensive applications.
pg_duckdb was developed in collaboration with our partners, Hydra and MotherDuck.

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
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} || /bin/true

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} || /bin/true

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/lib/libduckdb.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%exclude %{pginstdir}/lib/bitcode/*

%changelog
* Wed Dec 24 2025 Vonng <rh@vonng.com> - 1.1.1-1PIGSTY
* Tue Dec 16 2025 Vonng <rh@vonng.com> - 1.1.0-2PIGSTY
* Sun Nov 01 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- this is not published yet, but for pg_mooncake building 7daa8e53a
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.3.1-1PIGSTY
* Wed Dec 11 2024 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
* Thu Oct 24 2024 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- the first public release, used by Pigsty <https://pigsty.io>
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>