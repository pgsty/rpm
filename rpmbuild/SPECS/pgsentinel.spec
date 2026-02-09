%global pname pgsentinel
%global sname pgsentinel
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension providing Active session history
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL provides session activity. However, in order to gather activity behavior,
users have to sample the pg_stat_activity view multiple times.
pgsentinel is an extension to record active session history and link the activity
with query statistics (pg_stat_statements).

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
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{pname}-%{version}

%build
cd src
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd src
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
- https://github.com/pgsentinel/pgsentinel/releases/tag/v1.4.0
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 1.3.1-1PIGSTY
* Thu Nov 20 2025 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
* Fri May 23 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
