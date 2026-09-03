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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.5
Release:	1PGSTY%{?dist}
Summary:	Rewrite SQL statements with a PostgreSQL ProcessUtility hook
License:	PostgreSQL
URL:		https://github.com/pierreforstmann/pg_query_rewrite
Source0:	%{sname}-%{version}.tar.gz
#           repacked from upstream master snapshot commit 2f3e0c80027fc98a5fcb7be0e951abd3676baa56

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_query_rewrite translates matching SQL statements to predefined target SQL
through a ProcessUtility hook. It must be loaded via shared_preload_libraries
before CREATE EXTENSION is run in each database that should use the rewrite
rules.

%prep
%setup -q -n %{sname}-master

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%doc CHANGELOG
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.0.5-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.0.5-1PIGSTY
- Package upstream master snapshot 2f3e0c8 carrying extension version 0.0.5
