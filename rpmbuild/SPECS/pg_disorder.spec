%global pname pg_disorder
%global sname pg_disorder
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_disorder only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        Perturb unordered SELECT results to expose test failures
License:        PostgreSQL
URL:            https://github.com/viralpraxis/pg_disorder
Source0:        %{sname}-%{version}.tar.gz
#               normalized from https://api.pgxn.org/dist/pg_disorder/0.1.0/pg_disorder-0.1.0.zip

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pg_disorder is a test-only PostgreSQL module that reverses or shuffles rows
from eligible top-level SELECT statements without ORDER BY. It is loaded with
session_preload_libraries and is not intended for production use.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
  PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot} \
  PG_CONFIG=%{pginstdir}/bin/pg_config

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.1.0
