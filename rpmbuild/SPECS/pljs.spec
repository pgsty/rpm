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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.5
Release:	1PGSTY%{?dist}
Summary:	Trusted JavaScript Language Extension for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/plv8/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/plv8/pljs/archive/refs/tags/v1.0.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
PLJS is a trusted JavaScript language extension for PostgreSQL.
It is compact, lightweight, and fast, using the QuickJS JavaScript engine.
PLJS can be used for stored procedures, triggers, and more.

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
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.5-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Feb 07 2026 Vonng <rh@vonng.com> - 1.0.5-1PIGSTY
- https://github.com/plv8/pljs/releases/tag/v1.0.5
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 1.0.4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
