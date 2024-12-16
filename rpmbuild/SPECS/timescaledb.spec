%global debug_package %{nil}
%global sname	timescaledb

Summary:	PostgreSQL based time-series database
Name:		%{sname}_%{pgmajorversion}
Version:	2.17.2
Release:	1PGDG%{?dist}
License:	Timescale
Source0:	https://github.com/timescale/%{sname}/archive/%{version}.tar.gz
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

%package devel
Summary:	Development portions of timescaledb-tsl
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires:	perl-Test-Harness

%description devel
This packages includes development portions of timescaledb-tsl.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?rhel} && 0%{?rhel} == 7
%patch -P 1 -p0
%endif

# Disable telemetry, so that we can distribute it via PGDG repos:
export PATH=%{pginstdir}/bin:$PATH
./bootstrap -DSEND_TELEMETRY_DEFAULT=NO \
	-DREGRESS_CHECKS=OFF

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

%files devel
%{pginstdir}/lib/pgxs/src/test/perl/AccessNode.pm
%{pginstdir}/lib/pgxs/src/test/perl/DataNode.pm
%{pginstdir}/lib/pgxs/src/test/perl/TimescaleNode.pm

%changelog
* Mon Dec 16 2024 Vonng <rh@vonng.com> - 2.17.2
- Initial RPM release, used by Pigsty <https://pigsty.io>