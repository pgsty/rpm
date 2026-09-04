%global pname pointcloud
%global sname pointcloud
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
Version:	1.2.5
Release:	1PGSTY%{?dist}
Summary:	A PostgreSQL extension for storing point cloud (LIDAR) data
License:	BSD-3-Clause
URL:		https://github.com/pgpointcloud/pointcloud
Source0:	pointcloud-%{version}.tar.gz
#           https://github.com/pgpointcloud/pointcloud/archive/refs/tags/v1.2.5.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
A PostgreSQL extension for storing point cloud (LIDAR) data.
See https://pgpointcloud.github.io/pointcloud/ for more information.

%prep
%setup -q -n %{sname}-%{version}

%build
%set_build_flags
PATH=%{pginstdir}/bin:$PATH ./autogen.sh
PATH=%{pginstdir}/bin:$PATH ./configure
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}*.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}_postgis.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.5-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Oct 11 2023 Vonng <rh@vonng.com> - 1.2.5
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
