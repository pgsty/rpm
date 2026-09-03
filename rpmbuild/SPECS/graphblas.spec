%global sname graphblas

Name:           %{sname}
Version:        10.5.0
Release:        1PGSTY%{?dist}
Summary:        SuiteSparse implementation of the GraphBLAS standard
License:        Apache-2.0
URL:            https://github.com/DrTimothyAldenDavis/GraphBLAS
Source0:        graphblas-%{version}.tar.gz

BuildRequires:  cmake >= 3.23
BuildRequires:  gcc
BuildRequires:  make

%description
SuiteSparse:GraphBLAS is a complete implementation of the GraphBLAS standard
for sparse linear algebra and graph algorithms. This package provides the
shared library libgraphblas.so.10.

%package devel
Summary:        Development files for SuiteSparse:GraphBLAS
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and CMake package files for SuiteSparse:GraphBLAS.

%prep
%setup -q -n GraphBLAS-%{version}

%build
%set_build_flags
cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DGRAPHBLAS_COMPACT=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DSUITESPARSE_USE_FORTRAN=OFF \
  -DSUITESPARSE_DEMOS=OFF
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
%{_libdir}/libgraphblas.so.10*

%files devel
%{_includedir}/suitesparse/GraphBLAS.h
%{_libdir}/libgraphblas.so
%{_libdir}/pkgconfig/GraphBLAS.pc
%{_libdir}/cmake/GraphBLAS/*

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 10.5.0-1PGSTY
- Update SuiteSparse:GraphBLAS to 10.5.0 with libgraphblas.so.10 ABI retained
- Use upstream's distro-recommended compact mode with the CPU JIT enabled

* Tue Jul 28 2026 Vonng <rh@vonng.com> - 10.2.0-2PIGSTY
- Match the normalized lowercase source archive root

* Mon Apr 13 2026 Vonng <rh@vonng.com> - 10.2.0-1PIGSTY
- Package SuiteSparse:GraphBLAS 10.2.0 as runtime and devel RPMs
