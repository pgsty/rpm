%global pname biscuit
%global sname biscuit
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%ifarch x86_64
%if 0%{?rhel} && 0%{?rhel} == 9
%{!?llvm:%global llvm 0}
%else
%{!?llvm:%global llvm 1}
%endif
%else
%{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.4.3
Release:	1PIGSTY%{?dist}
Summary:	IAM-LIKE pattern matching with bitmap indexing
License:	MIT
URL:		https://github.com/CrystallineCore/Biscuit
Source0:	Biscuit-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/biscuit/2.4.3/biscuit-2.4.3.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
Biscuit is a PostgreSQL Index Access Method (IAM) for high-performance pattern matching
on text columns. Biscuit indexes are specifically designed to accelerate LIKE queries with
arbitrary wildcards using roaring bitmaps. It provides superior performance for wildcard
pattern matching compared to traditional B-tree, GIN, or GiST indexes, especially for
queries with leading wildcards like '%%pattern%%'.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
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
%setup -q -n Biscuit-%{version}
sed -i '1i .DEFAULT_GOAL := all' Makefile
# PostgreSQL packages on EL9 x86_64 inject -flto=auto through pg_config,
# which trips gcc's LTO jobserver path for this PGXS build.
%ifarch x86_64
%if 0%{?rhel} == 9
sed -i '/^[[:space:]]*-fPIC$/a override CFLAGS += -fno-lto' Makefile
%endif
%endif

%build
%if %llvm
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config LLVM_BINPATH=%{llvm_binpath}
%else
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config with_llvm=no
%endif

%install
%{__rm} -rf %{buildroot}
%if %llvm
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}
%else
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot} with_llvm=no
%endif

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
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
