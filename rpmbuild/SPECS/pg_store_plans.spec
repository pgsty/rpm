%global pname pg_store_plans
%global sname pg_store_plans
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.10
Release:	1PGSTY%{?dist}
Summary:	Store execution plans like pg_stat_statements does for queries
License:	BSD-3-Clause
URL:		https://github.com/ossc-db/%{sname}/
Source0:	https://repo.pigsty.cc/ext/%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
The pg_store_plans module provides a means for tracking execution plan
statistics of all SQL statements executed by a server.

The module must be loaded by adding pg_store_plans to
shared_preload_libraries in postgresql.conf, because it requires
additional shared memory. This means that a server restart is required
to add or remove the module.

%prep
%setup -q -n %{pname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.10-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Apr 06 2026 Vonng <rh@vonng.com> - 1.10-1PIGSTY
- https://github.com/ossc-db/pg_store_plans/releases/tag/1.10
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 1.9-1PIGSTY
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 1.8-2PIGSTY
* Sat Nov 02 2024 Vonng <rh@vonng.com> - 1.8-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
