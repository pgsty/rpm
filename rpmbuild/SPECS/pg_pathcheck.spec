%define debug_package %{nil}
%global pname pg_pathcheck
%global sname pg_pathcheck
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

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_pathcheck 0.9.1 pg17-18 branch supports PostgreSQL 17 and 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.9.1
Release:	1PIGSTY%{?dist}
Summary:	Validate planner Path trees for freed or corrupt memory
License:	MIT
URL:		https://github.com/danolivo/pg_pathcheck
Source0:	%{sname}-%{version}-pg17-18.tar.gz
#           normalized from https://codeload.github.com/danolivo/pg_pathcheck/tar.gz/refs/heads/pg17-18
#           Preload-only module; no CREATE EXTENSION objects are registered.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc perl
Requires:	postgresql%{pgmajorversion}-server

%description
pg_pathcheck is a PostgreSQL planner diagnostics module that walks Path trees
and reports freed, corrupt, or alias-recycled nodes using NodeTag and parent
checks. It registers no SQL objects and must be loaded through
shared_preload_libraries. This package uses the upstream pg17-18 branch for
PostgreSQL 17 and 18.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Thu Apr 30 2026 Vonng <rh@vonng.com> - 0.9.1-1PIGSTY
- Initial RPM release for upstream pg17-18 branch version 0.9.1
- Package pg_pathcheck pg17-18 branch as a preload-only diagnostics module
