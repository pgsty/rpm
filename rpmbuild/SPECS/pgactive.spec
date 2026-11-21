%global pname pgactive
%global sname pgactive
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.10
Release:	1PGSTY%{?dist}
Summary:	Active-active Replication Extension for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/aws/pgactive
Source0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros libselinux-devel libxslt-devel pam-devel numactl-devel
%if 0%{?pgmajorversion} >= 15 && 0%{?pgmajorversion} < 19
BuildRequires: libpgfeutils%{pgmajorversion}
%endif
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%if 0%{?pgmajorversion} == 15
BuildRequires: postgresql15-devel >= 15.20
BuildRequires: libpgfeutils15 >= 15.20
Requires: postgresql15-server >= 15.20
%elif 0%{?pgmajorversion} == 16
BuildRequires: postgresql16-devel >= 16.16
BuildRequires: libpgfeutils16 >= 16.16
Requires: postgresql16-server >= 16.16
%elif 0%{?pgmajorversion} == 17
BuildRequires: postgresql17-devel >= 17.12
BuildRequires: libpgfeutils17 >= 17.12
Requires: postgresql17-server >= 17.12
%elif 0%{?pgmajorversion} == 18
BuildRequires: postgresql18-devel >= 18.7
BuildRequires: libpgfeutils18 >= 18.7
Requires: postgresql18-server >= 18.7
%elif 0%{?pgmajorversion} == 19
BuildRequires: postgresql19-devel >= 19.0
BuildRequires: postgresql19-static >= 19.0
Requires: postgresql19-server >= 19.0
%endif

%description
pgactive is a PostgreSQL replication extension for creating an active-active database.

%prep
%setup -q -n %{pname}-%{version}

%build
%set_build_flags
PATH=%{pginstdir}/bin:$PATH ./configure
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
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 2.1.10-1PGSTY
- Update to 2.1.10; use upstream control and shared-memory offset fixes.

* Fri Nov 06 2026 Vonng <rh@vonng.com> - 2.1.9-1PGSTY
- Fix byte offsets in shared lock state allocation

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.1.9-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- New upstream release
- Correct the upstream control default version
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 2.1.7-1PIGSTY
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 2.1.6-1PIGSTY
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 2.1.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
