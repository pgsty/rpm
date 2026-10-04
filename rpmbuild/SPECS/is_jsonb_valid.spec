%global pname is_jsonb_valid
%global sname is_jsonb_valid
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:is_jsonb_valid only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.4
Release:        1PGSTY%{?dist}
Summary:        Native JSON Schema validation for PostgreSQL
License:        MIT
URL:            https://github.com/furstenheim/is_jsonb_valid
Source0:        is_jsonb_valid-0.1.4-1f536758ae06.tar.gz
# Source: https://codeload.github.com/furstenheim/is_jsonb_valid/tar.gz/1f536758ae066a22378ecbbdb2ca3ba27a5ac6ce
# SHA256: 55836219b52d6040d85e0fe36feba694b8e74e3ae85284dd35ecbdf0c8fc3878

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Native JSON Schema validation for PostgreSQL.

%prep
%setup -q -n is_jsonb_valid-1f536758ae066a22378ecbbdb2ca3ba27a5ac6ce

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg}  %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/lib/%{pname}_draft_v7.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 0.1.4-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
