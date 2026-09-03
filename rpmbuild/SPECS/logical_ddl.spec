%global pname logical_ddl
%global sname logical_ddl
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
Summary:	Replicate supported DDL changes over PostgreSQL logical replication
License:	MIT
URL:		https://github.com/samedyildirim/logical_ddl
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/samedyildirim/logical_ddl/archive/refs/tags/v0.1.0.tar.gz
#           Supported: PostgreSQL 11+

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
logical_ddl captures selected ALTER TABLE operations with an event trigger,
stores them in replicated metadata tables, and replays compatible DDL changes
on logical replication subscribers to reduce schema drift between nodes.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/logical_ddl-0.1.0.patch

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%doc doc/logical_ddl.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/logical_ddl.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Fix upstream RAISE WARNING typo so CREATE EXTENSION succeeds
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
