%global debug_package %{nil}
%global sname timescaledb
%global pginstdir /usr/pgsql-%{pgmajorversion}

Summary:	PostgreSQL based time-series database
Name:		%{sname}-tsl_%{pgmajorversion}
Version:	2.22.0
Release:	1PIGSTY%{?dist}
License:	Timescale
Source0:	%{sname}-%{version}.tar.gz
URL:		https://github.com/timescale/timescaledb
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	openssl-devel

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake >= 3.4
%endif

Requires:	postgresql%{pgmajorversion}-server
Conflicts:	%{sname}_%{pgmajorversion}

%description
TimescaleDB is an open-source database designed to make SQL scalable for
time-series data. It is engineered up from PostgreSQL, providing automatic
partitioning across time and space (partitioning key), as well as full SQL
support.

%prep
%setup -q -n %{sname}-%{version}

# Disable telemetry
export PATH=%{pginstdir}/bin:$PATH
./bootstrap -DSEND_TELEMETRY_DEFAULT=NO -DREGRESS_CHECKS=OFF

%build
export PATH=%{pginstdir}/bin:$PATH
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
export CFLAGS
export CXXFLAGS

cd build; %{__make}

%install
export PATH=%{pginstdir}/bin:$PATH
cd build; %{__make} DESTDIR=%{buildroot} install

%files
%defattr(-, root, root)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%exclude %{pginstdir}/lib/pgxs/src/test/perl/AccessNode.pm
%exclude %{pginstdir}/lib/pgxs/src/test/perl/DataNode.pm
%exclude %{pginstdir}/lib/pgxs/src/test/perl/TimescaleNode.pm

%changelog
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 2.22.0
- https://github.com/timescale/timescaledb/releases/tag/2.21.1
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 2.21.1
- https://github.com/timescale/timescaledb/releases/tag/2.21.1
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 2.20.3
- https://github.com/timescale/timescaledb/releases/tag/2.20.3
* Fri May 23 2025 Vonng <rh@vonng.com> - 2.20.0
- https://github.com/timescale/timescaledb/releases/tag/2.20.0
* Wed May 07 2025 Vonng <rh@vonng.com> - 2.19.3
- https://github.com/timescale/timescaledb/releases/tag/2.19.3
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 2.19.1
- https://github.com/timescale/timescaledb/releases/tag/2.19.1
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 2.19.0
- https://github.com/timescale/timescaledb/releases/tag/2.19.0
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 2.18.2
- https://github.com/timescale/timescaledb/releases/tag/2.18.2
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 2.18.1
- https://github.com/timescale/timescaledb/releases/tag/2.18.1
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 2.18.0
- https://github.com/timescale/timescaledb/releases/tag/2.18.0
* Mon Dec 16 2024 Vonng <rh@vonng.com> - 2.17.2
- Initial RPM release, used by Pigsty <https://pigsty.io>