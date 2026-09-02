%global pname arraymath
%global sname pg_arraymath
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20260702
%global snapshot_commit 4822319968a5fa9000a521e2f46cc18ff737af66
%global snapshot_short 4822319

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
Version:	1.1
Release:	2.git%{snapshot_date}.%{snapshot_short}PGSTY%{?dist}
Summary:	Functions and operators for element-by-element math and logic on arrays
License:	MIT
URL:		https://github.com/pramsey/pgsql-arraymath
Source0:	pgsql-%{pname}-%{version}+git%{snapshot_date}.%{snapshot_short}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 clang llvm
Requires:	postgresql%{pgmajorversion}-server

%description
An extension for element-by-element operations on PostgreSQL arrays with a integer, float or numeric data type.

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
%setup -q -n pgsql-%{pname}-%{version}+git%{snapshot_date}.%{snapshot_short}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

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
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.1-2.git20260702.4822319PGSTY
- Package upstream master snapshot 4822319 with PG_MODULE_MAGIC_EXT
- Declare clang and llvm for PGXS bitcode generation

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
