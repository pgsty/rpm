%global pname biscuit
%global sname biscuit
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch x86_64
%if 0%{?rhel} && 0%{?rhel} == 9
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
Version:	3.1.0
Release:	1PGSTY%{?dist}
Summary:	IAM-LIKE pattern matching with bitmap indexing
License:	MIT
URL:		https://github.com/CrystallineCore/Biscuit
Source0:	Biscuit-%{version}.tar.gz
Patch0:		biscuit-3.1.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Biscuit is a PostgreSQL Index Access Method (IAM) for high-performance pattern matching
on text columns. Biscuit indexes are specifically designed to accelerate LIKE queries with
arbitrary wildcards using roaring bitmaps. It provides superior performance for wildcard
pattern matching compared to traditional B-tree, GIN, or GiST indexes, especially for
queries with leading wildcards like '%%pattern%%'.

%prep
%setup -q -n Biscuit-%{version}
%patch -P 0 -p1
sed -i '1i .DEFAULT_GOAL := all' Makefile
# PostgreSQL packages on EL9 x86_64 inject -flto=auto through pg_config,
# which trips gcc's LTO jobserver path for this PGXS build.
%ifarch x86_64
%if 0%{?rhel} == 9
sed -i '/^[[:space:]]*-fPIC$/a override CFLAGS += -fno-lto' Makefile
%endif
%endif

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 3.1.0-1PGSTY
- Update to 3.1.0

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 3.0.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Aug 12 2026 Vonng <rh@vonng.com> - 3.0.0-1PIGSTY
- Update to stable PGXN distribution 3.0.0
- Ship the WAL-logged on-disk format; existing 2.x indexes require REINDEX
- Restore the missing update path from packaged extension versions 2.4.0/2.4.1
- Drop the unused PostgreSQL contrib runtime dependency

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 2.4.3-1PIGSTY
- Update to latest stable PGXN distribution 2.4.3
- Package the upstream extension SQL/default version 2.4.1

* Wed Jul 01 2026 Vonng <rh@vonng.com> - 2.4.1-1PIGSTY
- Update package to upstream PGXN 2.4.1; extension SQL remains 2.4.0

* Tue Jun 30 2026 Vonng <rh@vonng.com> - 2.4.0-1PIGSTY
- Bump to upstream PGXN 2.4.0

* Thu Jun 18 2026 Vonng <rh@vonng.com> - 2.3.0-1PIGSTY
- Use upstream PGXN 2.3.0 to match extension metadata and SQL version
- Backport PG16 and PG17 API compatibility fixes for current active builds
- Disable JIT subpackages on EL9 x86_64 to avoid llvm-lto install crashes
- Disable PGXS gcc LTO on EL9 x86_64 to avoid link-time jobserver failures

* Fri Jun 12 2026 Vonng <rh@vonng.com> - 2.2.2-2PIGSTY
- Rename RPM packages from pg_biscuit_<pgmajorversion> to biscuit_<pgmajorversion>
- Use system llvm-lto path for PGXS JIT builds
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 2.2.2-1PIGSTY
* Tue Dec 16 2025 Vonng <rh@vonng.com> - 2.0.1-1PIGSTY
- repo goes to https://github.com/CrystallineCore/Biscuit
* Tue Nov 18 2025 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
