%global pname plv8
%global sname plv8
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:plv8 only supports PostgreSQL 15 through 19 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
# Use the compiler beside PGXS's llvm-lto. Newer system Clang bitcode can
# be unreadable by the LLVM library linked into the PostgreSQL JIT provider.
%global with_llvm_arg CLANG='$(LLVM_BINPATH)/clang'
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	3.2.5
Release:	2PGSTY%{?dist}
Summary:	V8 Engine Javascript Procedural Language add-on for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/plv8/plv8
Source0:    plv8-%{version}.tar.gz
Patch0:     plv8-3.2.5-v8-build.patch
#           https://github.com/plv8/plv8/archive/refs/tags/v3.2.5.tar.gz
#           includes v8-cmake at gitlink 90d6634d820af06f14c642a9ef3a7bfa7ab4667a

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	python3
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%if 0%{?rhel} == 9
# Current PGDG EL9 packages use the parallel LLVM 21 toolchain.
BuildRequires:	clang21 llvm21
%endif
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
PLV8 is a trusted Javascript language extension for PostgreSQL. It can be used for stored procedures, triggers, etc.

%prep
%setup -q -n %{sname}-%{version}
# Keep gcc/g++ as the V8 CMake compilers, pass V8_CFLAGS/V8_CXXFLAGS into the bundled
# engine, build only the V8 libraries plv8 links, link the architecture
# stack-scanner helper into mksnapshot and the module, and add the <algorithm>
# include that GCC 14+ requires.
patch -p1 --fuzz=0 < %{PATCH0}

%build
%set_build_flags
%if 0%{?rhel} >= 10
# V8 type-puns Node** and BasicBlock** in its scheduler. Match Chromium's
# aliasing contract under EL10's GCC 14 LTO to keep mksnapshot from crashing.
export CXXFLAGS="$CXXFLAGS -fno-strict-aliasing"
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} clean CXX=/usr/bin/g++
# Preserve the distribution debug flags in both the bundled V8 engine and
# plv8's own objects so the split debuginfo package contains full DWARF.
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} NUMPROC=%{_smp_build_ncpus} CXX=/usr/bin/g++ OPTFLAGS="-std=c++17 -fno-rtti $CXXFLAGS" V8_CFLAGS="$CFLAGS" V8_CXXFLAGS="$CXXFLAGS"

%install
%{__rm} -rf %{buildroot}
%set_build_flags
%if 0%{?rhel} >= 10
export CXXFLAGS="$CXXFLAGS -fno-strict-aliasing"
export QA_RPATHS=3
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} NUMPROC=%{_smp_build_ncpus} CXX=/usr/bin/g++ OPTFLAGS="-std=c++17 -fno-rtti $CXXFLAGS" V8_CFLAGS="$CFLAGS" V8_CXXFLAGS="$CXXFLAGS"

%files
%{pginstdir}/lib/%{pname}*.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Vonng <rh@vonng.com> - 3.2.5-2PGSTY
- Enable upstream PostgreSQL 19 support and target PostgreSQL 15 through 19
- Name the bundled V8 build patch by purpose and declare its Python dependency
- Match Clang to the PGXS LLVM toolchain and preserve V8 C/C++ debug information

* Wed Sep 30 2026 Vonng <rh@vonng.com> - 3.2.5-1PGSTY
- Preserve V8 aliasing semantics with GCC 14 LTO on EL10

* Tue Sep 29 2026 Vonng <rh@vonng.com> - 3.2.5-1PGSTY
- Update to upstream 3.2.5 with the pinned, verified V8 source bundle
- Rebase V8 build fixes and include the patch in the SRPM
- Order LLVM compilation after generated configuration headers
- Let PGXS use the C++ linker while V8 CMake keeps separate C/C++ compilers

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
