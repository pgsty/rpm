%define debug_package %{nil}
%global sname rdkit
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?rhel} && 0%{?rhel} < 10
%{error:rdkit is currently packaged only for EL10 in this repository}
%endif

Name:           %{sname}
Version:        202503.6
Release:        1PIGSTY%{?dist}
Summary:        RDKit runtime libraries and PostgreSQL cartridge with InChI enabled
License:        BSD-3-Clause
URL:            https://github.com/rdkit/rdkit
Source0:        rdkit_%{version}.orig.tar.xz
# mirrored from the PGDG/Debian source package orig tarball
Source1:        better-enums-0.11.3-enum.h
# mirrored from the upstream better-enums 0.11.3 header used by RDKit

BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  pgdg-srpm-macros >= 1.0.27
BuildRequires:  bison
BuildRequires:  boost-devel
BuildRequires:  cairo-devel
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gcc-c++
BuildRequires:  inchi-devel >= 1.07.3
BuildRequires:  make
BuildRequires:  rapidjson-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel

Requires:       inchi%{?_isa} >= 1.07.3

%description
RDKit is an open source cheminformatics toolkit. This package ships the shared
libraries and data files needed by the PostgreSQL RDKit cartridge, built with
system InChI support enabled on EL10.

%package devel
Summary:        Development files for RDKit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       inchi-devel >= 1.07.3

%description devel
Headers, shared library symlinks, and CMake metadata for building software
against the RDKit shared libraries.

%package -n %{sname}_%{pgmajorversion}
Summary:        RDKit cartridge for PostgreSQL %{pgmajorversion}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       postgresql%{pgmajorversion}-server

%description -n %{sname}_%{pgmajorversion}
The RDKit PostgreSQL cartridge adds molecule types, fingerprints, substructure
search, and InChI / InChIKey functions to PostgreSQL %{pgmajorversion}.

%prep
%setup -q -n rdkit-Release_2025_03_6
patch -p1 --forward -f < %{_specdir}/patches/rdkit-202503.6-skip-catch2-fetch-when-tests-disabled.patch
cp -f %{SOURCE1} Code/RDGeneral/enum.h

%build
PATH=%{pginstdir}/bin:$PATH cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DLIB_SUFFIX=64 \
  -DRDK_INSTALL_INTREE=OFF \
  -DRDK_INSTALL_STATIC_LIBS=OFF \
  -DRDK_BUILD_SWIG_WRAPPERS=OFF \
  -DRDK_BUILD_PYTHON_WRAPPERS=OFF \
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
  -DRDK_INSTALL_COMIC_FONTS=OFF \
  -DBoost_NO_BOOST_CMAKE=TRUE \
  -DINCHI_INCLUDE_DIR=%{_includedir}/inchi \
  -DINCHI_LIBRARY=%{_libdir}/libinchi.so \
  -DINCHI_LIBRARIES=%{_libdir}/libinchi.so \
  -DPostgreSQL_CONFIG=%{pginstdir}/bin/pg_config \
  -DPostgreSQL_INCLUDE_DIR=%{pginstdir}/include \
  -DPostgreSQL_TYPE_INCLUDE_DIR=%{pginstdir}/include/server \
  -DPostgreSQL_LIBRARY=%{pginstdir}/lib/libpq.so
cmake --build build %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build
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

%files -n %{sname}_%{pgmajorversion}
%{pginstdir}/lib/rdkit.so
%{pginstdir}/share/extension/rdkit.control
%{pginstdir}/share/extension/rdkit--*.sql

%changelog
* Mon Apr 13 2026 Vonng <rh@vonng.com> - 202503.6-1PIGSTY
- Package RDKit 202503.6 for EL10 with system InChI 1.07.3 enabled
- Ship runtime libraries, devel headers, and PostgreSQL cartridge subpackage
- Avoid FetchContent downloading Catch2 when C++ tests are disabled
- Vendor the upstream better-enums 0.11.3 header for offline RPM builds
- Pass INCHI_LIBRARIES explicitly so the PostgreSQL cartridge links libinchi
