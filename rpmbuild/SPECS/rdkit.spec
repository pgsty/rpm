%define debug_package %{nil}
%global sname rdkit
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?rhel} && 0%{?rhel} < 9
%{error:rdkit 2026.03.6 is currently packaged only for EL9 and later}
%endif

Name:           %{sname}
Version:        202603.6
Release:        1PGSTY%{?dist}
Summary:        RDKit runtime libraries and PostgreSQL cartridge with InChI enabled
License:        BSD-3-Clause
URL:            https://github.com/rdkit/rdkit
Source0:        rdkit_%{version}.orig.tar.xz
# reproducibly recompressed from the official Release_2026_03_6 tag archive
Source1:        better-enums-0.11.3-enum.h
# mirrored from the upstream better-enums 0.11.3 header used by RDKit
Patch0:         rdkit-202603.6.patch
Patch1:         rdkit-202603.6-extension-upgrade.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  pgdg-srpm-macros >= 1.0.27
BuildRequires:  bison
BuildRequires:  boost-devel
BuildRequires:  boost-numpy3
BuildRequires:  boost-python3
BuildRequires:  cairo-devel
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gcc-c++
BuildRequires:  inchi-devel >= 1.07.5
BuildRequires:  make
BuildRequires:  patchelf
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel

Requires:       inchi%{?_isa} >= 1.07.5

%description
RDKit is an open source cheminformatics toolkit. This package ships the shared
libraries and data files needed by the PostgreSQL RDKit cartridge, built with
system InChI support enabled on EL9 and later.

%package devel
Summary:        Development files for RDKit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       inchi-devel >= 1.07.5

%description devel
Headers, shared library symlinks, and CMake metadata for building software
against the RDKit shared libraries.

%package -n python3-rdkit
Summary:        Python 3 bindings for RDKit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-numpy

%description -n python3-rdkit
Python 3 bindings for RDKit molecule parsing, descriptors, fingerprints,
reactions, depictions, and InChI support.

%package -n %{sname}_%{pgmajorversion}
Summary:        RDKit cartridge for PostgreSQL %{pgmajorversion}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       postgresql%{pgmajorversion}-server

%description -n %{sname}_%{pgmajorversion}
The RDKit PostgreSQL cartridge adds molecule types, fingerprints, substructure
search, and InChI / InChIKey functions to PostgreSQL %{pgmajorversion}.

%prep
%setup -q -n rdkit-Release_2026_03_6
patch -p1 --fuzz=0 < %{PATCH0}
patch -p1 --fuzz=0 < %{PATCH1}
cp -f %{SOURCE1} Code/RDGeneral/enum.h

%build
PATH=%{pginstdir}/bin:$PATH cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_SKIP_RPATH=ON \
  -DLIB_SUFFIX=64 \
  -DRDK_INSTALL_INTREE=OFF \
  -DRDK_INSTALL_STATIC_LIBS=OFF \
  -DRDK_BUILD_SWIG_WRAPPERS=OFF \
  -DRDK_BUILD_PYTHON_WRAPPERS=ON \
  -DRDK_INSTALL_PYTHON_TESTS=OFF \
  -DRDK_BUILD_CPP_TESTS=OFF \
  -DRDK_BUILD_TEST_GZIP=OFF \
  -DRDK_BUILD_THREADSAFE_SSS=ON \
  -DRDK_BUILD_INCHI_SUPPORT=ON \
  -DRDK_BUILD_PGSQL=ON \
  -DRDK_PGSQL_STATIC=OFF \
  -DRDK_BUILD_AVALON_SUPPORT=OFF \
  -DRDK_BUILD_MOLINTERCHANGE_SUPPORT=ON \
  -DRDK_OPTIMIZE_POPCNT=OFF \
  -DRDK_USE_URF=OFF \
  -DRDK_BUILD_COORDGEN_SUPPORT=OFF \
  -DRDK_BUILD_MAEPARSER_SUPPORT=OFF \
  -DRDK_BUILD_CAIRO_SUPPORT=ON \
  -DRDK_BUILD_CHEMDRAW_SUPPORT=OFF \
  -DRDK_BUILD_PUBCHEMSHAPE_SUPPORT=OFF \
  -DRDK_BUILD_XYZ2MOL_SUPPORT=OFF \
  -DRDK_INSTALL_COMIC_FONTS=OFF \
  -DBoost_NO_BOOST_CMAKE=TRUE \
  -DPython_EXECUTABLE=%{__python3} \
  -DINCHI_INCLUDE_DIR=%{_includedir}/inchi \
  -DINCHI_LIBRARY=%{_libdir}/libinchi.so \
  -DINCHI_LIBRARIES=%{_libdir}/libinchi.so \
  -DPostgreSQL_CONFIG=%{pginstdir}/bin/pg_config \
  -DPostgreSQL_INCLUDE_DIR=%{pginstdir}/include \
  -DPostgreSQL_TYPE_INCLUDE_DIR=%{pginstdir}/include/server \
  -DPostgreSQL_LIBRARY=%{pginstdir}/lib/libpq.so
cmake --build build --parallel 2

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build
patchelf --remove-rpath %{buildroot}%{pginstdir}/lib/rdkit.so
%{__rm} -f %{buildroot}%{_libdir}/libRDKit*.a
%{__rm} -rf %{buildroot}%{_bindir}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc README.md
%doc ReleaseNotes.md
%{_libdir}/libRDKit*.so.1*
%{_datadir}/RDKit/*

%files devel
%{_includedir}/rdkit/*
%{_libdir}/libRDKit*.so
%{_libdir}/cmake/rdkit/*
%{_libdir}/cmake/rdkitpython/*

%files -n python3-rdkit
%{python3_sitearch}/rdkit

%files -n %{sname}_%{pgmajorversion}
%{pginstdir}/lib/rdkit.so
%{pginstdir}/share/extension/rdkit.control
%{pginstdir}/share/extension/rdkit--*.sql

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 202603.6-1PGSTY
- Update RDKit runtime, development files, Python bindings, and cartridge to 2026.03.6
- Enable the EL9 Boost 1.75 baseline and retain the InChI 1.07.5 dependency floor
- Adapt Boost.JSON 1.75 string views without disabling MolInterchange
- Remove two unused Boost.Unordered flat-set includes unavailable before Boost 1.81
- Strip build-tree RPATHs from the PostgreSQL cartridge payload
- Replace the retired RapidJSON input with upstream Boost.JSON MolInterchange support

* Mon Aug 31 2026 Pigsty <rh@vonng.com> - 202503.6-2PIGSTY
- Require the InChI 1.07.5 development ABI used by this build

* Mon Apr 13 2026 Vonng <rh@vonng.com> - 202503.6-1PIGSTY
- Vendor RapidJSON 1.1.0 as a build input to keep MolInterchange offline
- Package RDKit 202503.6 for EL10 with system InChI 1.07.3 enabled
- Ship runtime libraries, devel headers, and PostgreSQL cartridge subpackage
- Avoid FetchContent downloading Catch2 when C++ tests are disabled
- Vendor the upstream better-enums 0.11.3 header for offline RPM builds
- Pass INCHI_LIBRARIES explicitly so the PostgreSQL cartridge links libinchi
