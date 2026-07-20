%global pname pg_kpart
%global sname pg_kpart
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
%{error:pg_kpart 1.0 supports PostgreSQL 14 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PIGSTY%{?dist}
Summary:        Reject full partition scans that omit the partition key
License:        ISC
URL:            https://github.com/hexacluster/pg_kpart
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/hexacluster/pg_kpart/archive/refs/tags/v1.0.tar.gz

BuildRequires:  gcc
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_kpart installs a PostgreSQL planner hook that rejects queries which would
scan every partition of a partitioned table without a usable partition-key
predicate. The hook must be loaded through shared_preload_libraries or
session_preload_libraries; CREATE EXTENSION is optional and registers the
module in pg_extension.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*.bc
%{pginstdir}/lib/bitcode/%{pname}/*.bc
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 20 2026 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release for pg_kpart 1.0 and PostgreSQL 14 through 18
- https://github.com/hexacluster/pg_kpart/releases/tag/v1.0
