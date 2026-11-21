%global pname uint128
%global sname pg_uint128
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
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

%if 0%{?rhel} >= 10
# This module does not link PostgreSQL private libraries. EL10 rejects the
# redundant versioned PostgreSQL RUNPATH added by PGXS.
%global pgxs_rpath_arg enable_rpath=no
%else
%global pgxs_rpath_arg %{nil}
%endif

%if 0%{?rhel} == 8
# GCC 8 lacks __has_builtin, selecting upstream's unimplemented int128
# overflow fallback. Use a compiler that enables the existing builtins.
%global pgxs_cc_arg CC=/opt/rh/gcc-toolset-15/root/usr/bin/gcc
%else
%global pgxs_cc_arg %{nil}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:        1PGSTY%{?dist}
Summary:	A PostgreSQL extension that adds native support for unsigned integers and 128-bit signed/unsigned integer types.
License:	PostgreSQL
URL:		https://github.com/pg-uint/pg-uint128
Source0:	pg-uint128-%{version}.tar.gz
Patch0:        pg_uint128-1.3.0-pg19-int8-datum.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if 0%{?rhel} == 8
BuildRequires:	gcc-toolset-15-gcc gcc-toolset-15-annobin-plugin-gcc
%endif
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Native unsigned integer and signed/unsigned 128-bit types for PostgreSQL,
with arithmetic, comparison, casts, aggregates and range operators.

%prep
%setup -q -n pg-uint128-%{version}
%patch -P 0 -p1

%build
%if 0%{?rhel} == 8
source /opt/rh/gcc-toolset-15/enable
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{pgxs_rpath_arg} %{pgxs_cc_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%if 0%{?rhel} == 8
source /opt/rh/gcc-toolset-15/enable
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{pgxs_rpath_arg} %{pgxs_cc_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 1.3.0-1PGSTY
- Update to upstream 1.3.0.
- Use upstream operator fixes; retire the superseded 1.2.0 backports.
- Preserve signed 8-bit Datum conversions on PostgreSQL 19.

* Fri Nov 20 2026 Vonng <rh@vonng.com> - 1.2.0-2PGSTY
- Remove invalid arithmetic commutators rejected by PostgreSQL security updates
- Correct comparison commutators to prevent incorrect index scan results
- Preserve upstream arithmetic return types and existing extension SQL versions
- Omit the redundant PostgreSQL RUNPATH when building on EL10
- Use GCC Toolset 15 on EL8 to enable the existing int128 overflow builtins

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
- https://github.com/pg-uint/pg-uint128/releases/tag/1.2.0
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.1.1-1PIGSTY
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
* Sun Oct 20 2024 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
