%global pname pgsentinel
%global sname pgsentinel
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.5.1
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension providing Active session history
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
PostgreSQL provides session activity. However, in order to gather activity behavior,
users have to sample the pg_stat_activity view multiple times.
pgsentinel is an extension to record active session history and link the activity
with query statistics (pg_stat_statements).

%prep
%setup -q -n %{pname}-%{version}

%build
cd src
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd src
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif
%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 1.5.1-1PGSTY
- Update to 1.5.1.

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.5.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- https://github.com/pgsentinel/pgsentinel/releases/tag/v1.5.0
- Require PostgreSQL contrib for pg_stat_statements

* Mon Jul 20 2026 Vonng <rh@vonng.com> - 1.4.2-1PIGSTY
- https://github.com/pgsentinel/pgsentinel/releases/tag/v1.4.2
- Require PostgreSQL contrib for pg_stat_statements
* Sat Mar 21 2026 Vonng <rh@vonng.com> - 1.4.1-1PIGSTY
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
- https://github.com/pgsentinel/pgsentinel/releases/tag/v1.4.0
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 1.3.1-1PIGSTY
* Thu Nov 20 2025 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
* Fri May 23 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
