%global pname istore
%global sname istore
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:istore only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.12
Release:        1PGSTY%{?dist}
Summary:        Integer key/value types and aggregates for PostgreSQL
License:        MIT
URL:            https://github.com/adjust/istore
Source0:        istore-0.1.12.tar.gz
Patch0:         istore-0.1.12-pg16.patch
# Source: https://api.pgxn.org/dist/istore/0.1.12/istore-0.1.12.zip
# SHA256: 1c770a799e26527362c316ce1c360f54d2674ba9f24047a00145819398442242

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Integer key/value types and aggregates for PostgreSQL.

%prep
%setup -q -n istore-0.1.12
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg}  %{?_smp_mflags}

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
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 0.1.12-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
