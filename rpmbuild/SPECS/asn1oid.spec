%global pname asn1oid
%global sname asn1oid
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
Version:	1.6
Release:	2PGSTY%{?dist}
Summary:	ASN.1 OID datatype for PostgreSQL
License:	GPL-3.0-or-later
URL:		https://github.com/df7cb/pgsql-asn1oid
Source0:	pgsql-asn1oid-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
The asn1oid extension provides a datatype for ASN.1 OIDs in PostgreSQL.

%prep
%setup -q -n pgsql-asn1oid-%{version}

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
* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.6-2PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Rebuild with corrected license metadata.

* Thu Mar 20 2025 Vonng <rh@vonng.com> - 1.6
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.5
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
