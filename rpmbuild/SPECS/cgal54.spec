# Based on the PGDG EL8 source RPM; see bin/postgis-sources.json.
# The installed CGAL 5.x payload is header-only and architecture independent.
# Min dependencies
%global boost_version 1.66
%global qt_version 5.9
%global cmake_version 3.14

%global fullversion %{version}


Name:           CGAL
Version:        5.4.2
Release:        1PGSTY%{?dist}
BuildArch:      noarch
Summary:        Computational Geometry Algorithms Library

License:        LGPLv3+ and GPLv3+ and Boost
URL:            http://www.cgal.org/
Source0:        https://github.com/CGAL/cgal/releases/download/v%{fullversion}/%{name}-%{fullversion}.tar.xz

# Required devel packages.
BuildRequires: cmake >= %{cmake_version}
BuildRequires: gcc-c++
BuildRequires: gmp-devel
BuildRequires: boost-devel >= %{boost_version}
BuildRequires: mpfr-devel
BuildRequires: qt5-qtbase-devel >= %{qt_version}
BuildRequires: qt5-qtsvg-devel >= %{qt_version}
BuildRequires: qt5-qtscript-devel >= %{qt_version}
BuildRequires: qt5-qttools-devel >= %{qt_version}
BuildRequires: make

%description
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.


%package devel
Summary:        Development files and tools for CGAL applications
Provides:       CGAL-static = %{version}-%{release}
Requires:       cmake
Requires:       boost-devel >= %{boost_version}
Requires:       gmp-devel
Requires:       mpfr-devel
Recommends:     zlib-devel
Recommends:     eigen3-devel
%description devel
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.
The %{name}-devel package provides the headers files and tools you may need to
develop applications using CGAL.



%package qt5-devel
Summary:        Development files and tools for CGAL applications using CGAL_Qt5
Requires:       %{name}-devel = %{version}-%{release}
Requires:       qt5-qtbase-devel >= %{qt_version}
Requires:       qt5-qtsvg-devel >= %{qt_version}
Requires:       qt5-qtscript-devel >= %{qt_version}
Requires:       qt5-qttools-devel >= %{qt_version}
%description qt5-devel
The %{name}-qt5-devel package provides the headers files and tools you
may need to develop applications using the CGAL_Qt5 component of CGAL.


%package demos-source
Summary:        Examples and demos of CGAL algorithms
Requires:       %{name}-devel = %{version}-%{release}
%description demos-source
The %{name}-demos-source package provides the sources of examples and demos of
CGAL algorithms.


%prep
%setup -q -n %{name}-%{fullversion}

# Fix some file permissions
#chmod a-x include/CGAL/export/ImageIO.h

# Install README.Fedora here, to include it in %%doc
cat << 'EOF' > ./README.Fedora
Header-only
-----------
CGAL is a header-only library since version 5.0.

Packages
--------
In Fedora, the CGAL tarball is separated in several packages:
  - CGAL is empty since CGAL-5.0
  - CGAL-devel contains header files, and several files and tools needed to
  develop CGAL applications,
  - CGAL-demos-source contains the source of examples and demos of CGAL.


Documentation
-------------
Note that the CGAL documentation cannot be packaged for Fedora due to unclear
license conditions. The complete documentation in PDF and HTML is
available at http://www.cgal.org/Manual/index.html
EOF

%build
%set_build_flags

%cmake -DCGAL_DO_NOT_WARN_ABOUT_CMAKE_BUILD_TYPE=ON -DCGAL_INSTALL_LIB_DIR=%{_datadir} -DCGAL_INSTALL_DOC_DIR=
%cmake_build

%install
rm -rf %{buildroot}

%cmake_install

# Install demos and examples
mkdir -p %{buildroot}%{_datadir}/CGAL
touch -r demo %{buildroot}%{_datadir}/CGAL/
cp -a demo %{buildroot}%{_datadir}/CGAL/demo
cp -a examples %{buildroot}%{_datadir}/CGAL/examples

%check
%set_build_flags
rm -rf include/
mkdir build-example
cd build-example
cmake -L "-DCMAKE_PREFIX_PATH=%{buildroot}/usr" %{buildroot}%{_datadir}/CGAL/examples/Triangulation_2
make constrained_plus
ldd ./constrained_plus
./constrained_plus

%files devel
%license AUTHORS LICENSE LICENSE.BSL LICENSE.RFL LICENSE.LGPL LICENSE.GPL
%doc CHANGES.md README.Fedora
%{_includedir}/CGAL
%exclude %{_includedir}/CGAL/Qt
%dir %{_datadir}/CGAL
%{_datadir}/cmake/CGAL
%exclude %{_datadir}/cmake/CGAL/demo
%{_bindir}/*
%exclude %{_bindir}/cgal_make_macosx_app
%{_mandir}/man1/cgal_create_cmake_script.1.gz

%files qt5-devel
%{_includedir}/CGAL/Qt
%{_datadir}/cmake/CGAL/demo

%files demos-source
%{_datadir}/CGAL/demo
%{_datadir}/CGAL/examples
%exclude %{_datadir}/CGAL/*/*/skip_vcproj_auto_generation

%changelog
* Sun Oct 04 2026 Ruohang Feng <rh@vonng.com> - 5.4.2-1PGSTY
- Import PGDG CGAL headers and example sources for the EL8 SFCGAL build.
- Package the architecture-independent payload as noarch.

* Mon Aug 22 2022 Devrim Gündüz <devrim@gunduz.org> - 5.4.2-1
- Update to 5.4.2, and also add to RHEL 8 as well.

* Wed Jul 13 2022 Devrim Gündüz <devrim@gunduz.org> - 5.4.1-1
- Initial packaging for PostgreSQL RPM repository, to build
  SFCGAL package on RHEL 9. Took spec file, etc from Fedora.
