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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
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
BuildRequires:	gcc make pgsodium-libsodium-devel >= 1.0.22
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pgsodium is an encryption library extension for PostgreSQL using the
libsodium library for high level cryptographic algorithms.

pgsodium can be used a straight interface to libsodium, but it can also use
a powerful feature called Server Key Management where pgsodium loads an
external secret key into memory that is never accessible to SQL. This
inaccessible root key can then be used to derive sub-keys and keypairs by
key id. This id (type bigint) can then be stored instead of the derived key.

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 3.1.11-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Update to 3.1.11 with the mask_role security fix and IPcrypt
- Link private symbol-prefixed libsodium 1.0.22 without replacing system ABI

* Tue Oct 22 2024 Vonng <rh@vonng.com> - 3.1.9
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
