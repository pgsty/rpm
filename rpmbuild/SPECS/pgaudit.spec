%global sname pgaudit
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

# PGDG already uses pgaudit_<pgmajor> for PostgreSQL 16 and newer.
# Only repackage the PostgreSQL 14/15 branches to normalize their RPM names.
%if 0%{?pgmajorversion} == 14
%global pversion 1.6.3
%global legacy_name pgaudit16_14
%else
%if 0%{?pgmajorversion} == 15
%global pversion 1.7.1
%global legacy_name pgaudit17_15
%else
%{error:pgaudit is repackaged only for PostgreSQL 14 and 15; use PGDG for PostgreSQL 16 through 18}
%endif
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        %{pversion}
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL session and object audit logging
License:        PostgreSQL
URL:            https://www.pgaudit.org
Source0:        %{sname}-%{version}.tar.gz
# https://github.com/pgaudit/pgaudit/archive/refs/tags/1.6.3.tar.gz
# https://github.com/pgaudit/pgaudit/archive/refs/tags/1.7.1.tar.gz

BuildRequires:  gcc make openssl-devel krb5-devel
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server
# PGDG pgauditlogtofile still requires the historical package name.
Provides:       %{legacy_name} = %{version}-%{release}

%description
pgAudit provides detailed session and object audit logging through the
standard PostgreSQL logging facility. Load pgaudit through
shared_preload_libraries and run CREATE EXTENSION pgaudit before enabling
pgaudit.log to include object information in DDL audit records.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{sname}/
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%endif

%changelog
* Thu Nov 05 2026 Ruohang Feng <rh@vonng.com> - 1.6.3/1.7.1-1PGSTY
- Package upstream 1.6.3 for PostgreSQL 14 and 1.7.1 for PostgreSQL 15.
- Use pgaudit_<pgmajor> names and provide the historical PGDG names.
- Keep upstream SQL files, native debug packages and main-package bitcode.
