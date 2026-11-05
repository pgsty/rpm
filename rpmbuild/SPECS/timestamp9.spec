%global sname timestamp9
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:timestamp9 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.4.0
Release:        1PGSTY%{?dist}
Summary:        Nanosecond-resolution timestamps for PostgreSQL
License:        MIT
URL:            https://github.com/optiver/timestamp9
Source0:        timestamp9-timestamp9-%{version}.tar.gz
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cmake gcc make
Requires:       postgresql%{pgmajorversion}-server

%description
The timestamp9 extension provides timestamps with nanosecond resolution.

%prep
%setup -q -n timestamp9-timestamp9-%{version}
sed -i 's/cmake_minimum_required(VERSION 3.4)/cmake_minimum_required(VERSION 3.10)/' CMakeLists.txt

%build
%set_build_flags
PATH=%{pginstdir}/bin:$PATH cmake -S . -B build \
    -DPG_CONFIG=%{pginstdir}/bin/pg_config \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build --parallel ${CMAKE_BUILD_PARALLEL_LEVEL:-2}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build

%files
%license LICENSE
%{pginstdir}/lib/timestamp9.so
%{pginstdir}/share/extension/timestamp9.control
%{pginstdir}/share/extension/timestamp9--*.sql

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 1.4.0-1PGSTY
- Add upstream 1.4.0 with PostgreSQL 14 through 18 builds and debug packages
