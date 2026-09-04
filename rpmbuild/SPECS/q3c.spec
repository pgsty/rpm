%global pname q3c
%global sname q3c
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
Version:	2.0.5
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension for spatial indexing on a sphere
License:	GPL-2.0-only
URL:		https://github.com/segasai/q3c
Source0:	q3c-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 numactl-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
https://ui.adsabs.harvard.edu/abs/2006ASPC..351..735K/abstract

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc q3c.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/q3c.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.0.5-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Aug 10 2026 Vonng <rh@vonng.com> - 2.0.5-1PIGSTY
- https://github.com/segasai/q3c/releases/tag/v2.0.5
* Wed Feb 25 2026 Vonng <rh@vonng.com> - 2.0.2-1PIGSTY
- https://github.com/segasai/q3c/releases/tag/v2.0.2
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 2.0.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
