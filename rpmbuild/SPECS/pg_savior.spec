%global pname pg_savior
%global sname pg_savior
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
Version:	0.1.0
Release:	1PGSTY%{?dist}
Summary:	Prevent accidental data loss and risky schema changes
License:	MIT
URL:		https://github.com/viggy28/pg_savior
Source0:	pg_savior-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_savior/0.1.0/pg_savior-0.1.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_savior installs PostgreSQL hooks that block risky DML and DDL before they
run, including DELETE or UPDATE without a WHERE clause, large estimated row
changes, CREATE INDEX without CONCURRENTLY, unsafe ALTER TABLE operations,
TRUNCATE or DROP TABLE on large tables, and DROP DATABASE. The hook must be
loaded through shared_preload_libraries, session_preload_libraries, or LOAD
before CREATE EXTENSION registers the SQL objects in each database.
For maintenance DDL such as installing other extensions, use the
pg_savior.bypass GUC in that session or load pg_savior after those objects are
installed.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Apr 30 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Update pg_savior to upstream PGXN 0.1.0
- Package the new safety hooks and document the preload requirement

* Sat Nov 01 2025 Vonng <rh@vonng.com> - 0.0.1-2PIGSTY
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
