%global sname system_stats
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	4.1
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension for exposing system metrics
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#		https://github.com/EnterpriseDB/system_stats/archive/refs/tags/v4.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
system_stats exposes system metrics such as CPU, memory, disk, network, and
process information to PostgreSQL for monitoring use cases. Access is
restricted to superusers and the monitor_system_stats role created by the
extension.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/include/server/extension/%{sname}/
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/uninstall_%{sname}.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 4.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Aug 11 2026 Vonng <rh@vonng.com> - 4.1-1PIGSTY
- Update to 4.1
- https://github.com/EnterpriseDB/system_stats/releases/tag/v4.1
* Fri Apr 10 2026 Vonng <rh@vonng.com> - 4.0-1PIGSTY
- Initial RPM release
- https://github.com/EnterpriseDB/system_stats/releases/tag/v4.0
