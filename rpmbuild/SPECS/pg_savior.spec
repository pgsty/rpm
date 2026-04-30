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

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Prevent accidental data loss and risky schema changes
License:	MIT
URL:		https://github.com/viggy28/pg_savior
Source0:	pg_savior-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_savior/0.1.0/pg_savior-0.1.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
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
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Thu Apr 30 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Update pg_savior to upstream PGXN 0.1.0
- Package the new safety hooks and document the preload requirement

* Sat Nov 01 2025 Vonng <rh@vonng.com> - 0.0.1-2PIGSTY
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
