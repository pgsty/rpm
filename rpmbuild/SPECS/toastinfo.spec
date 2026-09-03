%global pname toastinfo
%global sname toastinfo
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
Version:	1.7
Release:	1PGSTY%{?dist}
Summary:	Show storage structure of varlena datatypes in PostgreSQL
License:	PostgreSQL
URL:		https://github.com/df7cb/toastinfo
Source0:	toastinfo-%{version}.tar.gz
#           https://deb.debian.org/debian/pool/main/t/toastinfo/toastinfo_1.7.orig.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension exposes the internal storage structure of variable-length datatypes, called varlena.
The function pg_toastinfo describes the storage form of a datum:
null for NULLs
ordinary for non-varlena datatypes
short inline varlena for varlena values up to 126 bytes (1 byte header)
long inline varlena, (un)compressed for varlena values up to 1GiB (4 bytes header)
toasted varlena, (un)compressed for varlena values up to 1GiB stored in TOAST tables
compressed varlenas show the compression method (pglz, lz4) in PG14+
The function pg_toastpointer returns a varlena's chunk_id oid in the corresponding TOAST table. It returns NULL on non-varlena input.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.7-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Jun 17 2026 Vonng <rh@vonng.com> - 1.7-1PIGSTY
- https://deb.debian.org/debian/pool/main/t/toastinfo/toastinfo_1.7.orig.tar.gz
* Sat Jun 06 2026 Vonng <rh@vonng.com> - 1.6-1PIGSTY
- https://deb.debian.org/debian/pool/main/t/toastinfo/toastinfo_1.6.orig.tar.gz
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 1.5
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.4
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
