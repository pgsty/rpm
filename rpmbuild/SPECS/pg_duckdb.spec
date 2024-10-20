%define debug_package %{nil}
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
Version:	0.0.1
Release:	f34ae06%{?dist}
Summary:	DuckDB-powered Postgres for high performance apps & analytics.
License:	MIT License
URL:		https://github.com/duckdb/pg_duckdb
Source0:	%{sname}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
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
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} || /bin/true

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} || /bin/true

%files
%doc README.md
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


* Thu Oct 20 2024 Vonng <rh@vonng.com> -0.0.1-f34ae06
- https://github.com/duckdb/pg_duckdb/commit/d663d8a178ba8e9387dd9124e91dff1455afa2bf
* Mon Aug 12 2024 Vonng <rh@vonng.com> - 0.0.1
- Initial RPM release, used by Pigsty <https://pigsty.io>