%global pname pg_dirtyread
%global sname pg_dirtyread
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

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
Version:	2.8
Release:	1PIGSTY%{?dist}
Summary:	Read dead but unvacuumed tuples from a PostgreSQL relation
License:	PostgreSQL
URL:		https://github.com/df7cb/pg_dirtyread
Source0:	pg_dirtyread-%{version}.tar.gz
#           https://deb.debian.org/debian/pool/main/p/pg-dirtyread/pg-dirtyread_2.8.orig.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_dirtyread extension provides the ability to read dead but unvacuumed rows from a relation.
Supports PostgreSQL 9.2 and later. (On 9.2, at least 9.2.9 is required.)

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
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

%files
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
* Sat Jun 06 2026 Vonng <rh@vonng.com> - 2.8-1PIGSTY
- https://deb.debian.org/debian/pool/main/p/pg-dirtyread/pg-dirtyread_2.8.orig.tar.gz
* Fri Jun 14 2024 Vonng <rh@vonng.com> - 2.7
* Sun May 05 2024 Vonng <rh@vonng.com> - 2.6
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
