%global pname pg_json_diff
%global sname pg_json_diff
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_json_diff only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PGSTY%{?dist}
Summary:        JSON diff, patch and merge functions for PostgreSQL
License:        MIT
URL:            https://github.com/KhaledSMQ/pg-jsondiff
Source0:        pg_json_diff-1.0-95cd668636ce.tar.gz
# Source: https://codeload.github.com/KhaledSMQ/pg-jsondiff/tar.gz/95cd668636ce9c88d2f6ac57d92ac5301a81ed3c
# SHA256: 925fed2c6471b35f8b04cabcdf516c3a9c1c3f052a8395401a95385c214b9db6
Patch0:         pg-json-diff-1.0-control.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc-c++
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
JSON diff, patch and merge functions for PostgreSQL.

%prep
%setup -q -n pg-jsondiff-95cd668636ce9c88d2f6ac57d92ac5301a81ed3c
%patch -P 0 -p1

%build
%set_build_flags
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} CXXFLAGS="$CXXFLAGS -fPIC" %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.0-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
