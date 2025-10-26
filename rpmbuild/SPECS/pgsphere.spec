%global pname pg_sphere
%global sname pgsphere
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
Version:	1.5.2
Release:	1PIGSTY%{?dist}
Summary:	PgSphere provides spherical data types, functions, operators, and indexing for PostgreSQL.
License:	BSD 3-Clause
URL:		https://github.com/postgrespro/pgsphere
Source0:	pgsphere-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pgSphere is a PostgreSQL extension for spherical geometry.
This is an R-tree implementation using GiST for spherical objects like
spherical points and spherical circles with useful functions and operators.
It also supports the Block Range INdexing (BRIN) for large datasets.

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
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif


%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_HEALPIX=0 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_HEALPIX=0 install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/*.%{pname}
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.5.2-1PIGSTY
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.5.1-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>