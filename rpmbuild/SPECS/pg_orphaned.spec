%global pname pg_orphaned
%global sname pg_orphaned
%global gitdate 20260427
%global commit 4e23c9c3379bdedc878d585a3d81f7f4d5151993
%global shortcommit 4e23c9c
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_orphaned supports PostgreSQL 14 through 18 in Pigsty}
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	2.git%{gitdate}.%{shortcommit}PGSTY%{?dist}
Summary:	Allow to manipulate orphaned files thanks to a few functions
License:	PostgreSQL
URL:		https://github.com/bdrouvot/pg_orphaned
Source0:	%{sname}-git%{gitdate}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Allow to manipulate orphaned files thanks to a few functions:

pg_list_orphaned(interval): to list orphaned files. Orphaned files older than the interval parameter (default 1 Day) are listed with the "older" field set to true.
pg_move_orphaned(interval): to move orphaned files to a "orphaned_backup" directory. Only orphaned files older than the interval parameter (default 1 Day) are moved.
pg_list_orphaned_moved(): to list the orphaned files that have been moved to the "orphaned_backup" directory.
pg_move_back_orphaned(): to move back the orphaned files from the "orphaned_backup" directory to their orginal location (if still orphaned).
pg_remove_moved_orphaned(): to remove the orphaned files located in the "orphaned_backup" directory.

%prep
%setup -q -n %{sname}-%{commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.0-2.git20260427.4e23c9cPGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Update to upstream snapshot 4e23c9c from 2026-04-27
- Add PostgreSQL 18 compatibility while retaining extension SQL version 1.0

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
