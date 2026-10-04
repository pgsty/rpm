%global pname colnames
%global sname colnames
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:colnames only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.7.1
Release:        1PGSTY%{?dist}
Summary:        Return the column names of a PostgreSQL record
License:        PostgreSQL
URL:            https://github.com/theory/colnames
Source0:        %{sname}-%{version}.tar.gz
# Source: https://codeload.github.com/theory/colnames/tar.gz/refs/tags/v1.7.1
# SHA256: e62a0edfc21d56aaa58235c49ee7579695c4639518569e4df864aef0a09787dc
# Distribution 1.7.1 intentionally retains extension/control version 1.7.0.

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
colnames(record) returns the column names of a composite value as a name array.
It supports generic triggers and dynamic SQL without additional dependencies.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DOCS= DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md Changes doc/colnames.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.7.1-1PGSTY
- Initial package of upstream release 1.7.1, extension version 1.7.0
