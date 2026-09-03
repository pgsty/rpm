%global pname table_log
%global sname table_log
%global pginstdir /usr/pgsql-%{pgmajorversion}

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
Version:	0.6.4
Release:	1PGSTY%{?dist}
Summary:	Log changes on a table and restore the state of table/row on any time in the past
License:	PostgreSQL
URL:		https://github.com/df7cb/table_log
Source0:	%{sname}-0.6.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
table_log is a set of functions to log changes on a table in PostgreSQL and to restore the state of the table or a specific row on any time in the past.

For now it contains 2 functions:

table_log() -- log changes to another table
table_log_restore_table() -- restore a table or a specific column
NOTE: you can only restore a table where the original table and the logging table has a primary key!

This means: you can log everything, but for the restore function you must have a primary key on the original table (and of course a different pkey on the log table).

In the beginning (for table_log()) i have used some code from noup.c (you will find this in the contrib directory), but there should be no code left from noup, since i rewrote everything during the development. In fact, it makes no difference since both software is licensed with the BSD style licence which is used by PostgreSQL.

%prep
%setup -q -n %{sname}-0.6.4

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/table_log.md
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.6.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.6.4
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 0.6.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
