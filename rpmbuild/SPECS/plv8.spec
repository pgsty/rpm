%define debug_package %{nil}
%global pname plv8
%global sname plv8
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
Version:	3.2.4
Release:	2PIGSTY%{?dist}
Summary:	V8 Engine Javascript Procedural Language add-on for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/plv8/plv8
SOURCE0:    plv8-%{version}.tar.gz
#           https://github.com/plv8/plv8/archive/refs/tags/v3.2.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++
BuildRequires:	cmake
Requires:	postgresql%{pgmajorversion}-server

%description
PLV8 is a trusted Javascript language extension for PostgreSQL. It can be used for stored procedures, triggers, etc.

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
%if 0%{?rhel} >= 10
# EL10 exports CC/CXX during the RPM build setup and exposes two upstream build issues:
# plv8's Makefile passes g++ as the C compiler to v8-cmake, and the bundled
# v8-cmake needs minor source fixes for GCC 14 plus direct linkage of the
# conservative stack-scanner helper into both mksnapshot and the final module.
patch -p1 --forward -f < %{_specdir}/patches/plv8-3.2.4-el10-build-fixes.patch
%endif

%build
PATH=%{pginstdir}/bin:$PATH %{__make} clean
PATH=%{pginstdir}/bin:$PATH %{__make}

%install
%{__rm} -rf %{buildroot}
%if 0%{?rhel} >= 10
export QA_RPATHS=3
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}*.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 3.2.4-2PIGSTY
- fix EL10 builds and runtime loading by patching v8-cmake, direct stack-scanner linkage, and QA_RPATHS handling
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 3.2.4
* Sun Oct 13 2024 Vonng <rh@vonng.com> - 3.2.3
* Sun May 05 2024 Vonng <rh@vonng.com> - 3.2.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
