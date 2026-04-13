%define debug_package %{nil}
%global sname lagraph

Name:           %{sname}
Version:        1.2.1
Release:        1PIGSTY%{?dist}
Summary:        Graph algorithms and test harness built on GraphBLAS
License:        BSD-2-Clause
URL:            https://github.com/GraphBLAS/LAGraph
Source0:        lagraph-%{version}.tar.gz

BuildRequires:  cmake >= 3.20
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  graphblas-devel >= 10.2.0

Requires:       graphblas%{?_isa} >= 10.2.0

%description
LAGraph is a library plus test harness for collecting graph algorithms that
use GraphBLAS. This package provides the shared libraries liblagraph.so.1 and
liblagraphx.so.1.

%package devel
Summary:        Development files for LAGraph
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       graphblas-devel >= 10.2.0

%description devel
Headers, pkg-config metadata, and CMake package files for LAGraph.

%prep
%setup -q -n LAGraph-%{version}

%build
cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DGraphBLAS_ROOT=%{_prefix} \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF
cmake --build build %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_libdir}/liblagraph.so.1*
%{_libdir}/liblagraphx.so.1*

%files devel
%{_includedir}/suitesparse/LAGraph.h
%{_includedir}/suitesparse/LAGraphX.h
%{_libdir}/liblagraph.so
%{_libdir}/liblagraphx.so
%{_libdir}/pkgconfig/LAGraph.pc
%{_libdir}/cmake/LAGraph/*

%changelog
* Mon Apr 13 2026 Vonng <rh@vonng.com> - 1.2.1-1PIGSTY
- Package LAGraph 1.2.1 as runtime and devel RPMs, including LAGraphX
