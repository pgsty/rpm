%global sname pg_bulkload
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global pgbulkloadmajver 3
%global pgbulkloadmidver 1
%global pgbulkloadminver 23
%global	pgbulkloadpackagever %{pgbulkloadmajver}_%{pgbulkloadmidver}_%{pgbulkloadminver}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgbulkloadmajver}.%{pgbulkloadmidver}.%{pgbulkloadminver}
Release:	1PGSTY%{?dist}
URL:		https://github.com/ossc-db/%{sname}
Source0:	https://repo.pigsty.cc/ext/%{sname}-VERSION%{pgbulkloadpackagever}.tar.gz
#           https://github.com/ossc-db/%{sname}/archive/VERSION%{pgbulkloadpackagever}.tar.gz
License:	BSD-3-Clause
BuildRequires:	postgresql%{pgmajorversion}-devel openssl-devel pam-devel
BuildRequires:	libsepol-devel readline-devel krb5-devel numactl-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server %{sname}_%{pgmajorversion}-client

%description
pg_bulkload is a high speed data loading tool for PostgreSQL.

pg_bulkload is designed to load huge amount of data to a database. You can
load data to table bypassing PostgreSQL shared buffers.

pg_bulkload also has some ETL features; input data validation and data
transformation.

%package client
Summary:	High speed data loading utility for PostgreSQL
Requires:	postgresql%{pgmajorversion}-libs

%description client
pg_bulkload client subpackage provides client-only tools.

%prep
%setup -q -n %{sname}-VERSION%{pgbulkloadpackagever}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/pg_timestamp.so
%{pginstdir}/share/contrib/pg_timestamp.sql
%{pginstdir}/share/contrib/uninstall_pg_timestamp.sql
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp/*.bc
%endif

%files client
%defattr(-,root,root)
%{pginstdir}/bin/%{sname}
%{pginstdir}/bin/postgresql

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 3.1.23-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Jan 16 2026 Vonng <rh@vonng.com> - 3.1.23-1PIGSTY
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 3.1.22-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
