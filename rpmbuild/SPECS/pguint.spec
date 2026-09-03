%global pname uint
%global sname pguint
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
Version:    1.20260630
Release:    1PGSTY%{?dist}
License:    PostgreSQL
Summary:	Unsigned and other extra integer types for PostgreSQL
URL:		https://github.com/petere/%{sname}
Source0:    %{sname}-%{version}.tar.gz
#Source0:        https://github.com/petere/%{sname}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This extension provides additional integer types for PostgreSQL:
* int1 (signed 8-bit integer)
* uint1 (unsigned 8-bit integer)
* uint2 (unsigned 16-bit integer)
* uint4 (unsigned 32-bit integer)
* uint8 (unsigned 64-bit integer)

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.20260630-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 1.20260630

* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.20250815-1PIGSTY
* Sat Nov 02 2024 Vonng <rh@vonng.com> - 1.20231206-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
