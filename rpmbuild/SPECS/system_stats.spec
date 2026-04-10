%global sname system_stats
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	4.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension for exposing system metrics
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#		https://github.com/EnterpriseDB/system_stats/archive/refs/tags/v4.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
system_stats exposes system metrics such as CPU, memory, disk, network, and
process information to PostgreSQL for monitoring use cases. Access is
restricted to superusers and the monitor_system_stats role created by the
extension.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/include/server/extension/%{sname}/
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/uninstall_%{sname}.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Apr 10 2026 Vonng <rh@vonng.com> - 4.0-1PIGSTY
- Initial RPM release
- https://github.com/EnterpriseDB/system_stats/releases/tag/v4.0
