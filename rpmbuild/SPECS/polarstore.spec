%global sdk_version 1.2.42
%global pfs_commit d0c5dc6
%define debug_package %{nil}

Name:           polarstore
Version:        %{sdk_version}
Release:        1PIGSTY%{?dist}
Summary:        PolarStore PFSD SDK for PolarDB
License:        Apache-2.0
URL:            https://github.com/ApsaraDB/PolarDB-FileSystem
Source0:        polarstore-%{version}-%{pfs_commit}.tar.gz
BuildRequires:  cmake, gcc, gcc-c++, make
BuildRequires:  zlog, libaio-devel

%description
PolarStore PFSD SDK files built from PolarDB-FileSystem source and used by
PolarDB for PostgreSQL builds with --with-pfsd. This package installs the
PFSD header and static library under /usr/local/polarstore/pfsd.

%prep
%setup -q -n PolarDB-FileSystem-%{pfs_commit}
sed -i -e 's|cmake_minimum_required (VERSION 2.8)|cmake_minimum_required (VERSION 3.5)|' CMakeLists.txt
sed -i -e 's|-march=native ||g' CMakeLists.txt
sed -i -e 's|-Werror|-Werror -Wno-array-bounds|g' CMakeLists.txt
sed -i -e 's|calloc(sizeof(chnl_ctx_shm_t), 1)|calloc(1, sizeof(chnl_ctx_shm_t))|g' src/pfs_sdk/pfsd_chnl_shm.cc src/pfsd/pfsd_chnl_shm.cc

%build
cmake -S . -B obj -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build obj --target pfsd -j%{_smp_build_ncpus}

%install
install -d %{buildroot}/usr/local/polarstore/pfsd/include
install -d %{buildroot}/usr/local/polarstore/pfsd/lib
install -m 0644 src/pfs_sdk/pfsd_sdk.h %{buildroot}/usr/local/polarstore/pfsd/include/
install -m 0644 lib/libpfsd.a %{buildroot}/usr/local/polarstore/pfsd/lib/

%files
/usr/local/polarstore/pfsd/include/pfsd_sdk.h
/usr/local/polarstore/pfsd/lib/libpfsd.a

%changelog
* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.2.42-1PIGSTY
- Build PolarStore PFSD SDK from PolarDB-FileSystem source
