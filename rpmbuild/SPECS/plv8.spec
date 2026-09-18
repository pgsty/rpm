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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	3.2.4
Release:	1PGSTY%{?dist}
Summary:	V8 Engine Javascript Procedural Language add-on for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/plv8/plv8
Source0:    plv8-%{version}.tar.gz
#           https://github.com/plv8/plv8/archive/refs/tags/v3.2.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++
BuildRequires:	cmake
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
PLV8 is a trusted Javascript language extension for PostgreSQL. It can be used for stored procedures, triggers, etc.

%prep
%setup -q -n %{sname}-%{version}
# Keep gcc/g++ as the V8 CMake compilers, pass V8_CXXFLAGS into the bundled
# engine, build only the V8 libraries plv8 links, link the architecture
# stack-scanner helper into mksnapshot and the module, and add the <algorithm>
# include that GCC 14+ requires.
patch -p1 --forward -f < %{_specdir}/patches/plv8-3.2.4.patch

%build
%set_build_flags
PATH=%{pginstdir}/bin:$PATH %{__make} clean CC=/usr/bin/gcc CXX=/usr/bin/g++
# Preserve the distribution debug flags in both the bundled V8 engine and
# plv8's own objects so the split debuginfo package contains full DWARF.
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} NUMPROC=%{_smp_build_ncpus} CC=/usr/bin/gcc CXX=/usr/bin/g++ OPTFLAGS="-std=c++17 -fno-rtti $CXXFLAGS" V8_CXXFLAGS="$CXXFLAGS"

%install
%{__rm} -rf %{buildroot}
%set_build_flags
%if 0%{?rhel} >= 10
export QA_RPATHS=3
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} NUMPROC=%{_smp_build_ncpus} CC=/usr/bin/gcc CXX=/usr/bin/g++ OPTFLAGS="-std=c++17 -fno-rtti $CXXFLAGS" V8_CXXFLAGS="$CXXFLAGS"

%files
%{pginstdir}/lib/%{pname}*.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sun Sep 06 2026 Vonng <rh@vonng.com> - 3.2.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Keep the bundled CMake C and C++ compiler identities distinct
- Consolidate the build fixes into a single plv8-3.2.4.patch for every EL release
- Preserve full RPM debug flags in bundled V8 and wrapper C++ objects
- Link the architecture stack scanner into mksnapshot and the final module
- Build only the bundled V8 libraries required by the extension

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 3.2.4-2PIGSTY
- fix EL10 builds and runtime loading by patching v8-cmake, direct stack-scanner linkage, and QA_RPATHS handling
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 3.2.4
* Sun Oct 13 2024 Vonng <rh@vonng.com> - 3.2.3
* Sun May 05 2024 Vonng <rh@vonng.com> - 3.2.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
