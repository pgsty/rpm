%global pname pg_disorder
%global sname pg_disorder
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_disorder only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PIGSTY%{?dist}
Summary:        Perturb unordered SELECT results to expose test failures
License:        PostgreSQL
URL:            https://github.com/viralpraxis/pg_disorder
Source0:        %{sname}-%{version}.tar.gz
#               normalized from https://api.pgxn.org/dist/pg_disorder/0.1.0/pg_disorder-0.1.0.zip

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc
Requires:       postgresql%{pgmajorversion}-server

%description
pg_disorder is a test-only PostgreSQL module that reverses or shuffles rows
from eligible top-level SELECT statements without ORDER BY. It is loaded with
session_preload_libraries and is not intended for production use.

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
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} \
  PG_CONFIG=%{pginstdir}/bin/pg_config LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} \
  PG_CONFIG=%{pginstdir}/bin/pg_config LLVM_BINPATH=%{llvm_binpath}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Aug 07 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.1.0
