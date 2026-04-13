%global pname pg_query_rewrite
%global sname pg_query_rewrite
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

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_query_rewrite supports PostgreSQL 14-18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.5
Release:	1PIGSTY%{?dist}
Summary:	Rewrite SQL statements with a PostgreSQL ProcessUtility hook
License:	PostgreSQL
URL:		https://github.com/pierreforstmann/pg_query_rewrite
Source0:	%{sname}-%{version}.tar.gz
#           repacked from upstream master snapshot commit 2f3e0c80027fc98a5fcb7be0e951abd3676baa56

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
Requires:	postgresql%{pgmajorversion}-server

%description
pg_query_rewrite translates matching SQL statements to predefined target SQL
through a ProcessUtility hook. It must be loaded via shared_preload_libraries
before CREATE EXTENSION is run in each database that should use the rewrite
rules.

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
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-master

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%doc CHANGELOG
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.0.5-1PIGSTY
- Package upstream master snapshot 2f3e0c8 carrying extension version 0.0.5
