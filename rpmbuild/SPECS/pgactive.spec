%global pname pgactive
%global sname pgactive
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.9
Release:	1PGSTY%{?dist}
Summary:	Active-active Replication Extension for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/aws/pgactive
Source0:    %{sname}-%{version}.tar.gz
Patch0:     pgactive-2.1.9.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros libselinux-devel libxslt-devel pam-devel numactl-devel
%if %{pgmajorversion} >= 14
BuildRequires: libpgfeutils%{pgmajorversion}
%endif
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pgactive is a PostgreSQL replication extension for creating an active-active database.

%prep
%setup -q -n %{pname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
%set_build_flags
./configure
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%license LICENSE
%attr(0755,root,root) %{pginstdir}/bin/pgactive_dump
%attr(0755,root,root) %{pginstdir}/bin/pgactive_init_copy
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.1.9-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- New upstream release
- Correct the upstream control default version
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 2.1.7-1PIGSTY
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 2.1.6-1PIGSTY
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 2.1.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
