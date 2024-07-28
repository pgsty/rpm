%define debug_package %{nil}
%global pname pg_proctab
%global sname pg_proctab
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
Version:	0.0.10
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension to access the operating system process table.
License:	BSD 3-Clause License
URL:		https://gitlab.com/pg_proctab/pg_proctab
Source0:	pg_proctab-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL extension to access the operating system process table.

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
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif


%prep
%setup -q -n %{sname}-%{version}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make USE_PGXS=1 install DESTDIR=%{buildroot}

%files
%{pginstdir}/bin/*.sh
%{pginstdir}/bin/*.pl
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/doc/extension/README*
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.0.10
- Initial RPM release, used by Pigsty <https://pigsty.io>