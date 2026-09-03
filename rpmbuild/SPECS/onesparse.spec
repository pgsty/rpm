%global pname onesparse
%global sname onesparse
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

%if 0%{?pgmajorversion} != 18
%{error:onesparse only supports PostgreSQL 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PGSTY%{?dist}
Summary:	Sparse linear algebra and graph extension for PostgreSQL 18
License:	Apache-2.0
URL:		https://github.com/OneSparse/OneSparse
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc pkgconf-pkg-config
BuildRequires:	graphblas-devel >= 10.2.0
BuildRequires:	lagraph-devel >= 1.2.1
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	graphblas%{?_isa} >= 10.2.0
Requires:	lagraph%{?_isa} >= 1.2.1

%description
OneSparse exposes sparse vectors, matrices, and graph algorithms to PostgreSQL
through GraphBLAS- and LAGraph-backed data types and functions. The upstream
v1.0.0 release currently targets PostgreSQL 18 and ships extension SQL version
0.1.0 inside the release tarball.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/onesparse-1.0.0.patch

%build
PATH=%{pginstdir}/bin:$PATH PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Package official upstream release v1.0.0 for PostgreSQL 18
- Depend on packaged GraphBLAS/LAGraph RPMs and use only system pkg-config metadata
- Note that upstream release v1.0.0 ships extension SQL version 0.1.0
