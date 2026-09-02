%global pname pgsodium
%global sname pgsodium
%global pginstdir /usr/pgsql-%{pgmajorversion}
%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgsodium supports PostgreSQL 14 through 18}
%endif

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
Version:	3.1.11
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension for high level cryptographic algorithms
License:	PostgreSQL AND BSD-2-Clause AND MIT AND ISC
URL:		https://github.com/michelp/pgsodium
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pgsodium-3.1.11.patch

#https://git.postgresql.org/gitweb/?p=pgrpms.git;a=blob;f=rpm/redhat/main/non-common/pgsodium/main/pgsodium.spec;h=15127595c2645c2b57f121d55fdd8ed5cbaa3ab3;hb=HEAD

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang gcc llvm make pgsodium-libsodium-devel >= 1.0.22
Requires:	postgresql%{pgmajorversion}-server

%description
pgsodium is an encryption library extension for PostgreSQL using the
libsodium library for high level cryptographic algorithms.

pgsodium can be used a straight interface to libsodium, but it can also use
a powerful feature called Server Key Management where pgsodium loads an
external secret key into memory that is never accessible to SQL. This
inaccessible root key can then be used to derive sub-keys and keypairs by
key id. This id (type bigint) can then be stored instead of the derived key.

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
%autosetup -p1 -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

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
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 3.1.11-1PGSTY
- Update to 3.1.11 with the mask_role security fix and IPcrypt
- Link private symbol-prefixed libsodium 1.0.22 without replacing system ABI

* Tue Oct 22 2024 Vonng <rh@vonng.com> - 3.1.9
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
