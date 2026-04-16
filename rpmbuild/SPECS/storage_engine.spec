%define debug_package %{nil}
%global pname storage_engine
%global sname storage_engine
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
Version:	1.0.5
Release:	1PIGSTY%{?dist}
Summary:	Column-oriented and row-compressed table access methods for PostgreSQL
License:	AGPL-3.0
URL:		https://github.com/saulojb/storage_engine
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/saulojb/storage_engine/archive/refs/tags/v1.0.5.tar.gz
#           Supported: PostgreSQL 13, 14, 15, 16, 17, 18
#           Patch: shared build compatibility patch for configure metadata and PG16-18 headers

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libcurl-devel
BuildRequires:	lz4-devel
BuildRequires:	libzstd-devel

Requires:	postgresql%{pgmajorversion}-server

%description
storage_engine is a Hydra-derived PostgreSQL extension that provides two
high-performance table access methods: colcompress for column-oriented
analytics and rowcompress for row-based batch-compressed storage. It adds
vectorized execution, parallel scans, stripe-level pruning, and PostgreSQL
13-18 compatibility while remaining installable as a standard extension.

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
patch -p1 --forward -f < %{_specdir}/patches/storage_engine-1.0.5-build-compat.patch

%build
%configure PG_CONFIG=%{pginstdir}/bin/pg_config
%{__make} %{?_smp_mflags}

%install
%make_install

%files
%license LICENSE
%doc README.md BENCHMARKS.md CHANGELOG.md NOTICE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%{pginstdir}/include/server/citus_version.h
%exclude /usr/lib/.build-id/*
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Thu Apr 16 2026 Vonng <rh@vonng.com> - 1.0.5-1PIGSTY
- Initial RPM release for saulojb/storage_engine v1.0.5
- Package the Hydra-derived storage engine fork with PostgreSQL 13-18 support
- Share the same 1.0.5 compatibility patch with the DEB recipe for configure metadata and PG16-18 build fixes
