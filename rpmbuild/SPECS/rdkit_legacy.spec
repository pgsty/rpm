%define debug_package %{nil}
%global sname rdkit
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?rhel} && (0%{?rhel} < 8 || 0%{?rhel} > 9)
%{error:rdkit_legacy is only for EL8 and EL9}
%endif

Name:           %{sname}
Version:        202303.3
Release:        1PIGSTY%{?dist}
Summary:        RDKit runtime libraries and PostgreSQL cartridges
License:        BSD-3-Clause
URL:            https://github.com/rdkit/rdkit
Source0:        rdkit_202303.3.orig.tar.xz
# Imported from the official PGDG source package:
# https://apt.postgresql.org/pub/repos/apt/pool/main/r/rdkit/
Patch0:         rdkit-202303.3-pg16.patch
Patch1:         rdkit-202303.3-postgres-makefile.patch
Patch2:         rdkit-202303.3-pg17-operators.patch
Patch3:         rdkit-202303.3-skip-catch2-fetch-when-tests-disabled.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  bison
BuildRequires:  boost-devel
BuildRequires:  cairo-devel
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel

%description
RDKit is an open source cheminformatics toolkit. This compatibility build ships
the runtime libraries, development files, and PostgreSQL cartridge for EL8 and
EL9. Optional InChI support is disabled on these legacy targets.

%package devel
Summary:        Development files for RDKit
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, shared library symlinks, and CMake metadata for building software
against the RDKit shared libraries.

%package -n %{sname}_%{pgmajorversion}
Summary:        RDKit cartridge for PostgreSQL %{pgmajorversion}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       postgresql%{pgmajorversion}-server

%description -n %{sname}_%{pgmajorversion}
The RDKit PostgreSQL cartridge for PostgreSQL %{pgmajorversion}.

%prep
%setup -q -n rdkit-Release_2023_03_3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cmake -S . -B build \
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
  -DRDK_BUILD_INCHI_SUPPORT=OFF \
  -DRDK_BUILD_PGSQL=OFF \
  -DRDK_BUILD_AVALON_SUPPORT=OFF \
  -DRDK_BUILD_MOLINTERCHANGE_SUPPORT=OFF \
  -DRDK_OPTIMIZE_POPCNT=OFF \
  -DRDK_USE_URF=OFF \
  -DRDK_BUILD_COORDGEN_SUPPORT=OFF \
  -DRDK_BUILD_MAEPARSER_SUPPORT=OFF \
  -DRDK_BUILD_CAIRO_SUPPORT=ON \
  -DRDK_BUILD_CHEMDRAW_SUPPORT=OFF \
  -DRDK_BUILD_PUBCHEMSHAPE_SUPPORT=OFF \
  -DRDK_INSTALL_COMIC_FONTS=OFF \
  -DBoost_NO_BOOST_CMAKE=TRUE
cmake --build build %{?_smp_mflags}

%{__make} -C Code/PgSQL/rdkit clean \
  PG_CONFIG=%{pginstdir}/bin/pg_config \
  RDBASE=%{_builddir}/rdkit-Release_2023_03_3 \
  RDKIT_LIBDIR=%{_builddir}/rdkit-Release_2023_03_3/build/lib \
  STATIC_LINK=0 \
  with_llvm=no
PATH=%{pginstdir}/bin:$PATH \
  %{__make} -C Code/PgSQL/rdkit %{?_smp_mflags} \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    RDBASE=%{_builddir}/rdkit-Release_2023_03_3 \
    RDKIT_LIBDIR=%{_builddir}/rdkit-Release_2023_03_3/build/lib \
    STATIC_LINK=0 \
    with_llvm=no

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build
%{__rm} -f %{buildroot}%{_libdir}/libRDKit*.a
%{__rm} -rf %{buildroot}%{_bindir}

install -D -m 0755 Code/PgSQL/rdkit/rdkit.so %{buildroot}%{pginstdir}/lib/rdkit.so
install -D -m 0644 Code/PgSQL/rdkit/rdkit.control %{buildroot}%{pginstdir}/share/extension/rdkit.control
install -m 0644 Code/PgSQL/rdkit/rdkit--*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 Code/PgSQL/rdkit/update_sql/*.in %{buildroot}%{pginstdir}/share/extension/
for f in %{buildroot}%{pginstdir}/share/extension/*.in; do
  sed 's/@RDKIT_PARALLEL_SAFE@/PARALLEL SAFE/g' "$f" > "${f%.in}"
  rm -f "$f"
done

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
* Thu Jul 23 2026 Vonng <rh@vonng.com> - 202303.3-1PIGSTY
- Restore a maintained EL8 and EL9 recipe parameterized by PostgreSQL major
- Package runtime and development files from the same core library build
- Backport PostgreSQL 16-18 compatibility fixes and disable LLVM bitcode
- Avoid downloading Catch2 when C++ tests are disabled
