%global pname pgpcre
%global sname pgpcre
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

%if 0%{?rhel} >= 10
%{error:pgpcre requires the legacy PCRE 1 development package and only supports EL8 and EL9}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.20190509
Release:	1PGSTY%{?dist}
Summary:	PCRE functions for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/petere/pgpcre
Source0:	pgpcre-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	pcre-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This is a module for PostgreSQL that exposes Perl-compatible regular expressions (PCRE)
functionality as functions and operators. It is based on the popular PCRE library.

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
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.20190509-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Add the complete LLVM toolchain needed for PGXS bitcode and llvmjit payload

* Tue Jul 28 2026 Vonng <rh@vonng.com> - 0.20190509-2PIGSTY
- Restrict builds to EL8 and EL9 where the legacy PCRE development package exists

* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.20190509-1PIGSTY
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
