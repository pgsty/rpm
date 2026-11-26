%global pname plphp
%global sname plphp
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:plphp only supports PostgreSQL 15 through 19 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.6
Release:        1PGSTY%{?dist}
Summary:        PHP procedural language for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/commandprompt/plPHP
Source0:        plphp-2.6.tar.gz
Patch0:        plphp-2.6-pg19-tuplestore.patch
# Source: https://codeload.github.com/commandprompt/plPHP/tar.gz/plphp-2.6
# SHA256: 73717c319f34e3e7dbb1e14adf2aff40b17aa63c75a45739b91253c5c1003927

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  php-devel >= 8.1
BuildRequires:  php-embedded >= 8.1
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
PHP procedural language for PostgreSQL.

%prep
%setup -q -n plPHP-plphp-2.6

%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} enable_rpath=no %{with_llvm_arg} PHP_LIBDIR=%{_libdir} PHP_LIBNAME=php %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} enable_rpath=no %{with_llvm_arg} PHP_LIBDIR=%{_libdir} PHP_LIBNAME=php install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Vonng <rh@vonng.com> - 2.6-1PGSTY
- Adapt PostgreSQL 19 APIs with version-conditional compatibility

* Sun Oct 04 2026 Vonng <rh@vonng.com> - 2.6-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
