%global pname pg_statement_rollback
%global sname pg_statement_rollback
%global pginstdir /usr/pgsql-%{pgmajorversion}
%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_statement_rollback 1.6 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        1.6
Release:        2PGSTY%{?dist}
Summary:        Server-side statement rollback for PostgreSQL
License:        ISC
URL:            https://github.com/HexaCluster/pg_statement_rollback
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/HexaCluster/pg_statement_rollback/archive/refs/tags/v1.6.tar.gz
Patch0:         pg_statement_rollback-1.6.patch

BuildRequires:  clang gcc llvm make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_statement_rollback provides server-side automatic savepoints so a client
can roll back only the failed statement and continue the current transaction.
It is a loadable module and intentionally installs no CREATE EXTENSION objects.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides LLVM bitcode for %{sname}.
%endif

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config \
    %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config \
    %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} %{buildroot}%{pginstdir}/doc/contrib/README.md \
    %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license COPYING
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/doc/extension/README-%{sname}.md
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 1.6-2PGSTY
- Backport upstream PR 8 resource-owner and memory-context fixes
- Release the automatic savepoint before portal creation for SET TRANSACTION

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.6-1PIGSTY
- Initial Pigsty RPM package for pg_statement_rollback 1.6
- Keep the upstream control file and SQL metadata out of this module-only package
