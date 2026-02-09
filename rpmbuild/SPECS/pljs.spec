%define debug_package %{nil}
%global pname pljs
%global sname pljs
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
Version:	1.0.5
Release:	1PIGSTY%{?dist}
Summary:	Trusted JavaScript Language Extension for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/plv8/%{sname}
SOURCE0:	%{sname}-%{version}.tar.gz
#           https://github.com/plv8/pljs/archive/refs/tags/v1.0.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PLJS is a trusted JavaScript language extension for PostgreSQL.
It is compact, lightweight, and fast, using the QuickJS JavaScript engine.
PLJS can be used for stored procedures, triggers, and more.

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
PATH=%{pginstdir}/bin:$PATH %{__make} clean
# Build quickjs with -fPIC for shared library compatibility
# closefrom() is only available in glibc 2.34+ (EL9+), not in EL8
%if 0%{?rhel} >= 9 || 0%{?fedora}
cd deps/quickjs && %{__make} libquickjs.a CFLAGS="-fPIC -O2 -g -Wall -Wno-array-bounds -Wno-format-truncation -Wno-infinite-recursion -fwrapv -D_GNU_SOURCE -DCONFIG_VERSION=\\\"2025-04-26\\\" -DHAVE_CLOSEFROM" && cd ../..
%else
cd deps/quickjs && %{__make} libquickjs.a CFLAGS="-fPIC -O2 -g -Wall -Wno-array-bounds -Wno-format-truncation -Wno-infinite-recursion -fwrapv -D_GNU_SOURCE -DCONFIG_VERSION=\\\"2025-04-26\\\"" && cd ../..
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sat Feb 07 2026 Vonng <rh@vonng.com> - 1.0.5-1PIGSTY
- https://github.com/plv8/pljs/releases/tag/v1.0.5
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 1.0.4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
