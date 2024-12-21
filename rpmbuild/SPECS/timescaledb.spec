%global debug_package %{nil}
%global sname timescaledb
%global pginstdir /usr/pgsql-%{pgmajorversion}

Summary:	PostgreSQL based time-series database
Name:		pg_%{sname}_%{pgmajorversion}
Version:	2.17.2
Release:	1PIGSTY%{?dist}
License:	Timescale
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/timescale/timescaledb/archive/2.17.2.tar.gz

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
* Mon Dec 16 2024 Vonng <rh@vonng.com> - 2.17.2
- Initial RPM release, used by Pigsty <https://pigsty.io>