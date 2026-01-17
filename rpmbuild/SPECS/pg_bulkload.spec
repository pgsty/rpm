%global sname pg_bulkload
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global pgbulkloadmajver 3
%global pgbulkloadmidver 1
%global pgbulkloadminver 23
%global	pgbulkloadpackagever %{pgbulkloadmajver}_%{pgbulkloadmidver}_%{pgbulkloadminver}

%{!?llvm:%global llvm 1}

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgbulkloadmajver}.%{pgbulkloadmidver}.%{pgbulkloadminver}
Release:	1PIGSTY%{?dist}
URL:		https://github.com/ossc-db/%{sname}
Source0:	https://repo.pigsty.cc/ext/%{sname}-VERSION%{pgbulkloadpackagever}.tar.gz
#           https://github.com/ossc-db/%{sname}/archive/VERSION%{pgbulkloadpackagever}.tar.gz
License:	BSD-3-Clause
BuildRequires:	postgresql%{pgmajorversion}-devel openssl-devel pam-devel
BuildRequires:	libsepol-devel readline-devel krb5-devel numactl-devel
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

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_bulkload
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This package provides JIT support for pg_bulkload
%endif

%prep
%setup -q -n %{sname}-VERSION%{pgbulkloadpackagever}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

# Strip .so files to produce -debug* packages properly on SLES.
%{__strip} %{buildroot}%{pginstdir}/lib/*.so

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

%files client
%defattr(-,root,root)
%{pginstdir}/bin/%{sname}
%{pginstdir}/bin/postgresql

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp/*.bc
%endif

%changelog
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 3.1.23-1PIGSTY
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 3.1.22-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
