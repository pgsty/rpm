%global sname credcheck
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:credcheck is packaged for PostgreSQL 14 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        6.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL username and password policy checks
License:        PostgreSQL
URL:            https://github.com/HexaCluster/credcheck
Source0:        %{sname}-%{version}.tar.gz
# https://github.com/HexaCluster/credcheck/archive/refs/tags/v6.0.tar.gz
# EL8 security supplement while PGDG still supplies the unpatched 4.7 release.
# Reuse PGDG on other platforms and retire this exception when EL8 is fixed.

BuildRequires:  gcc make openssl-devel krb5-devel
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server
Requires:       openssl-libs >= 1.1.1k

%description
credcheck enforces username and password policies, password history and
authentication limits. Load credcheck through shared_preload_libraries to
enable its hooks. CREATE EXTENSION installs the accompanying SQL objects.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*
%endif

%changelog
* Thu Oct 29 2026 Ruohang Feng <rh@vonng.com> - 6.0-1PGSTY
- Package upstream 6.0 as a scoped EL8 security supplement.
- Fix self ALTER ROLE privilege escalation when password_valid_until is set.
- Preserve upstream SQL upgrades, native debug packages and main-package bitcode.
