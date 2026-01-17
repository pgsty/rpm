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

Name:		%{sname}_%{pgmajorversion}
Version:	0.6.4
Release:	1PIGSTY%{?dist}
Summary:	Log changes on a table and restore the state of table/row on any time in the past
License:	PostgreSQL
URL:		https://github.com/df7cb/table_log
Source0:	%{sname}-0.6.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
table_log is a set of functions to log changes on a table in PostgreSQL and to restore the state of the table or a specific row on any time in the past.

For now it contains 2 functions:

table_log() -- log changes to another table
table_log_restore_table() -- restore a table or a specific column
NOTE: you can only restore a table where the original table and the logging table has a primary key!

This means: you can log everything, but for the restore function you must have a primary key on the original table (and of course a different pkey on the log table).

In the beginning (for table_log()) i have used some code from noup.c (you will find this in the contrib directory), but there should be no code left from noup, since i rewrote everything during the development. In fact, it makes no difference since both software is licensed with the BSD style licence which is used by PostgreSQL.


%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-0.6.4

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/table_log.md
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.6.4
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 0.6.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>