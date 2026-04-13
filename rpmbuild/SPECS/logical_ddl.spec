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

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Replicate supported DDL changes over PostgreSQL logical replication
License:	MIT
URL:		https://github.com/samedyildirim/logical_ddl
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/samedyildirim/logical_ddl/archive/refs/tags/v0.1.0.tar.gz
#           Supported: PostgreSQL 11+

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
Requires:	postgresql%{pgmajorversion}-server

%description
logical_ddl captures selected ALTER TABLE operations with an event trigger,
stores them in replicated metadata tables, and replays compatible DDL changes
on logical replication subscribers to reduce schema drift between nodes.

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
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/logical_ddl-0.1.0-fix-raise-warning-typo.patch

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%doc doc/logical_ddl.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/logical_ddl.md

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Fix upstream RAISE WARNING typo so CREATE EXTENSION succeeds
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
