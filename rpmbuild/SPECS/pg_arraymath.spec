%global pname arraymath
%global sname pg_arraymath
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20260702
%global snapshot_commit 4822319968a5fa9000a521e2f46cc18ff737af66
%global snapshot_short 4822319
%global source_version 1.1+git%{snapshot_date}.%{snapshot_short}

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
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PGSTY%{?dist}
Summary:	Functions and operators for element-by-element math and logic on arrays
License:	MIT
URL:		https://github.com/pramsey/pgsql-arraymath
Source0:	pgsql-%{pname}-%{source_version}.tar.gz
Patch0:        pg_arraymath-1.1-pg19-compat.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
An extension for element-by-element operations on PostgreSQL arrays with a integer, float or numeric data type.

%prep
%setup -q -n pgsql-%{pname}-%{source_version}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Wed Nov 25 2026 Ruohang Feng <rh@vonng.com> - 1.1.0-1PGSTY
- Use a short package version for upstream snapshot 4822319.

* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 1.1-2.git%{snapshot_date}.%{snapshot_short}PGSTY
- Add PostgreSQL 19 header and type compatibility.

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.1-2.git20260702.4822319PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Package upstream master snapshot 4822319 with PG_MODULE_MAGIC_EXT
- Declare clang and llvm for PGXS bitcode generation

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
