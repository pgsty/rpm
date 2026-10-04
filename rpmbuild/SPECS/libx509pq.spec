%global pname libx509pq
%global sname libx509pq
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:libx509pq only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.3
Release:        1PGSTY%{?dist}
Summary:        X.509 certificate parsing functions for PostgreSQL
License:        GPL-3.0-or-later
URL:            https://github.com/crtsh/libx509pq
Source0:        libx509pq-1.3-bed05c6e87d7.tar.gz
Patch0:         libx509pq-1.3-openssl11.patch
# Source: https://codeload.github.com/crtsh/libx509pq/tar.gz/bed05c6e87d79a98d79e42a1fac16386eead0c13
# SHA256: 4f840143f771b588e654073e7d12fe2cbfb46c8adeb8c6b386abb5b6b701d8e4

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  openssl-devel
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
X.509 certificate parsing functions for PostgreSQL.

%prep
%setup -q -n libx509pq-bed05c6e87d79a98d79e42a1fac16386eead0c13
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
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.3-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
