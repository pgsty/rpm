# Based on the PGDG EL9 source RPM; see bin/postgis-sources.json.
%global postgismajorversion 3.6
%global postgissomajorversion 3
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global sname	postgis
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:postgis only supports PostgreSQL 14 through 18}
%endif

%pgdg_set_gis_variables

# Override some variables:
%global	geosfullversion %geos314fullversion
%global	geosmajorversion %geos314majorversion
%global	geosinstdir %geos314instdir

%if 0%{?rhel} && 0%{?rhel} == 8
%global	gdalfullversion %gdal38fullversion
%global	gdalmajorversion %gdal38majorversion
%global	gdalinstdir %gdal38instdir
%global	projmajorversion %proj96majorversion
%global	projfullversion %proj96fullversion
%global	projinstdir %proj96instdir
%else
%global	gdalfullversion %gdal313fullversion
%global	gdalmajorversion %gdal313majorversion
%global	gdalinstdir %gdal313instdir
%global	projmajorversion %proj98majorversion
%global	projfullversion %proj98fullversion
%global	projinstdir %proj98instdir
%endif

%{!?llvm:%global llvm 1}

# Propagate %%llvm into the actual build: PGXS decides whether to invoke
# clang/llvm-config based on with_llvm from the installed postgresql*-devel's
# Makefile.global, not from this spec's %%llvm. Without passing with_llvm=no
# through to make, setting %%llvm 0 here only drops the llvm BuildRequires/
# subpackage/files, while the build still tries to run clang regardless.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

%{!?utils:%global	utils 1}
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 1}
%{!?raster:%global	raster 1}

%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1500
%{!?sfcgal:%global	sfcgal 1}
%endif
%if 0%{?rhel} == 8
%ifarch ppc64 ppc64le
%{!?sfcgal:%global	sfcgal 0}
%else
%{!?sfcgal:%global	sfcgal 1}
%endif
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.4
Release:        1PGSTY%{?dist}
%if 0%{?rhel} == 8
# EL8 otherwise seeds identical client binaries only with VERSION-RELEASE.
# Include the PG-specific package name so their build-id links can coexist.
%global _find_debuginfo_opts %{?_find_debuginfo_opts} --build-id-seed %{name}-%{version}-%{release}
%endif
License:        GPL-2.0-or-later
Source0:	https://download.osgeo.org/postgis/source/postgis-%{version}.tar.gz
Source2:	https://download.osgeo.org/postgis/docs/postgis-%{version}-en.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh

URL:		https://www.postgis.net/

BuildRequires:	postgresql%{pgmajorversion}-devel geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	libgeotiff%{libgeotiffmajorversion}-devel libxml2 libxslt
BuildRequires:	pgdg-srpm-macros >= 1.0.54 gmp-devel pcre2-devel
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8
Requires:	pcre2
%else
Requires:	libpcre2-8-0
%endif
%if 0%{?suse_version} >= 1500
Requires:	libgmp10
%else
Requires:	gmp
%endif
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1500
BuildRequires:	libjson-c-devel proj%{projmajorversion}-devel >= %{projfullversion}
%endif
%else
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion} flex json-c-devel
%endif
BuildRequires:	libxml2-devel
BuildRequires:  gcc gcc-c++ make autoconf automake libtool pkgconf-pkg-config perl patchelf
%if %{shp2pgsqlgui}
BuildRequires:	gtk2-devel > 2.8.0
%endif
%if %{sfcgal}
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9
BuildRequires:	SFCGAL SFCGAL-devel >= 2.1.0
%endif
%if 0%{?rhel} == 8 || 0%{?suse_version} >= 1500
BuildRequires:	SFCGAL SFCGAL-devel
%endif
%endif

%if %{raster}
BuildRequires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
Requires:	gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
%endif

%if 0%{?suse_version} >= 1500
Requires:	libprotobuf-c1
BuildRequires:	libprotobuf-c-devel
%else
# Fedora/RHEL:
Requires:	protobuf-c >= 1.1.0
BuildRequires:	protobuf-c-devel >= 1.1.0
%endif

%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion} geos%{geosmajorversion} >= %{geosfullversion}
Requires:	postgresql%{pgmajorversion}-contrib proj%{projmajorversion} >= %{projfullversion}
Requires:	libgeotiff%{libgeotiffmajorversion}
Requires:	hdf5
Requires:	gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
%if 0%{?suse_version} == 1500
Requires:	libjson-c5
Requires:	libxerces-c-3_2
BuildRequires:	libxerces-c-devel
%endif
%if 0%{?suse_version} == 1600
Requires:	libjson-c5
Requires:	libxerces-c-3_3
BuildRequires:	libxerces-c-devel
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8
Requires:	json-c xerces-c
BuildRequires:	xerces-c-devel
%endif

Provides:	%{sname} = %{version}-%{release}
Provides:       %{sname}3_%{pgmajorversion} = %{version}-%{release}

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

%package client
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Summary:	Client tools and their libraries of PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}

%description client
The %{name}-client package contains the client tools and their libraries
of PostGIS.

%package docs
BuildArch:      noarch
Summary:	Extra documentation for PostGIS

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%if %{shp2pgsqlgui}
%package	gui
Summary:	GUI for PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	gui
The %{name}-gui package provides a gui for PostGIS.
%endif

%if %utils
%package utils
BuildArch:      noarch
Summary:	The utils for PostGIS
Requires:	%{name} = %{version}-%{release} perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}

%description utils
The %{name}-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} %{sname}-%{version}.pdf

%build
%set_build_flags
LDFLAGS="-Wl,-rpath,%{geosinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
SFCGAL_LDFLAGS="$SFCGAL_LDFLAGS -L/usr/lib64"; export SFCGAL_LDFLAGS

LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -lgeos_c -L%{projinstdir}/lib64 -L%{gdalinstdir}/lib -L%{libgeotiffinstdir}/lib -ltiff -L/usr/lib64"; export LDFLAGS
CFLAGS="$CFLAGS -I%{gdalinstdir}/include"; export CFLAGS
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{projinstdir}/lib64/pkgconfig

autoconf

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
	--bindir=%{pginstdir}/bin/ \
	--datadir=%{pginstdir}/share/ \
	--mandir=%{_mandir}/%{name} \
	--enable-lto \
	--with-projdir=%{projinstdir} \
%if !%raster
	--without-raster \
%endif
%if %{sfcgal}
	--with-sfcgal=%{_bindir}/sfcgal-config \
%endif
%if %{shp2pgsqlgui}
	--with-gui \
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1500
	--with-protobuf \
%else
	--without-protobuf \
%endif
	--enable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=%{geosinstdir}/bin/geos-config \
	--with-gdalconfig=%{gdalinstdir}/bin/gdal-config

%if 0%{?rhel} && 0%{?rhel} == 8
# Strip -flto from generated Makefiles (breaks RHEL 8 static archive linking)
find . -name "Makefile" | xargs sed -i 's/-flto\b//g'
%endif

SHLIB_LINK="$SHLIB_LINK" %{__make} %{?_smp_mflags} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{sname}-%{postgissomajorversion}.so" %{with_llvm_arg}

%{__make} %{?_smp_mflags} -C extensions %{with_llvm_arg}

%if %utils
 SHLIB_LINK="$SHLIB_LINK" %{__make} %{?_smp_mflags} -C utils %{with_llvm_arg}
%endif

%install
%{__rm} -rf %{buildroot}
SHLIB_LINK="$SHLIB_LINK" %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} %{with_llvm_arg}

%if %utils
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Select the versioned GIS stack without absolute RPATHs rejected by RPM.
# Both PostgreSQL's bin/ and lib/ are two levels below /usr.
for elf in %{buildroot}%{pginstdir}/lib/*.so \
    %{buildroot}%{pginstdir}/bin/pgsql2shp \
    %{buildroot}%{pginstdir}/bin/shp2pgsql \
%if %{raster}
    %{buildroot}%{pginstdir}/bin/raster2pgsql \
%endif
%if %{shp2pgsqlgui}
    %{buildroot}%{pginstdir}/bin/shp2pgsql-gui \
%endif
    ; do
    patchelf --force-rpath --set-rpath '$ORIGIN/../lib:$ORIGIN/../../geos%{geosmajorversion}/lib64:$ORIGIN/../../proj%{projmajorversion}/lib64:$ORIGIN/../../gdal%{gdalmajorversion}/lib' "$elf"
done

# Create alternatives entries for common binaries
%post client
%{_sbindir}/update-alternatives --install %{_bindir}/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql %{pgmajorversion}0

# Drop alternatives entries for common binaries and man files
%postun client
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove postgis-pgsql2shp	%{pginstdir}/bin/pgsql2shp
	%{_sbindir}/update-alternatives --remove postgis-shp2pgsql	%{pginstdir}/bin/shp2pgsql
fi

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%license LICENSE.TXT
%{pginstdir}/bin/postgis
%{pginstdir}/bin/postgis_restore
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/legacy*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*topology*.sql
%{pginstdir}/lib/%{sname}-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%if %{sfcgal}
%{pginstdir}/lib/%{sname}_sfcgal-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}_sfcgal*.sql
%{pginstdir}/share/extension/%{sname}_sfcgal.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_upgrade.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_sfcgal.sql
%endif
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}_topology-%{postgissomajorversion}.so
%{pginstdir}/lib/address_standardizer-3.so
%{pginstdir}/share/extension/address_standardizer*.sql
%{pginstdir}/share/extension/address_standardizer*.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_legacy.sql
%if %{raster}
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis_legacy.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis_upgrade.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/uninstall_rtpostgis.sql
%{pginstdir}/share/extension/postgis_raster*.sql
%{pginstdir}/lib/postgis_raster-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}_raster.control
%endif
%{_mandir}/%{name}/man1/*

%if %llvm
   %{pginstdir}/lib/bitcode/address_standardizer*.bc
   %{pginstdir}/lib/bitcode/address_standardizer-3/*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgissomajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgissomajorversion}/*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgissomajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgissomajorversion}/*.bc
   %if %{raster}
     %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}*.bc
     %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}/*.bc
   %endif
   %if %{sfcgal}
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}.index.bc
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}/lwgeom_sfcgal.bc
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}/postgis_sfcgal_legacy.bc
   %endif
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/pgsql2shp
%if %{raster}
%attr(755,root,root) %{pginstdir}/bin/raster2pgsql
%endif
%attr(755,root,root) %{pginstdir}/bin/shp2pgsql
%attr(755,root,root) %{pginstdir}/bin/pgtopo_export
%attr(755,root,root) %{pginstdir}/bin/pgtopo_import
%{_mandir}/%{name}/man1/pgsql2shp*
%{_mandir}/%{name}/man1/pgtopo_*
%{_mandir}/%{name}/man1/shp2pgsql*

%files docs
%defattr(-,root,root)
%doc %{sname}-%{version}.pdf

%if %shp2pgsqlgui
%files gui
%defattr(-,root,root)
%{pginstdir}/bin/shp2pgsql-gui
%{pginstdir}/share/applications/shp2pgsql-gui.desktop
%{pginstdir}/share/icons/hicolor/*/apps/shp2pgsql-gui.png
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%changelog
* Sun Oct 04 2026 Ruohang Feng <rh@vonng.com> - 3.6.4-1PGSTY
- Import PGDG PostGIS 3.6.4 for PostgreSQL 14 through 18.
- Keep LLVM bitcode in the main package without an extension llvmjit package.
- Omit the empty devel package and correct client alternatives removal.
- Preserve RPM build flags and generate debuginfo and debugsource packages.
- Use origin-relative RPATHs to select the versioned GIS dependencies.
- Include the package name in EL8 build-id seeds for parallel PG installs.

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 3.6.4-1PGDG
- Update to 3.6.4 per changes described at:
  https://gitea.osgeo.org/postgis/postgis/raw/tag/3.6.4/NEWS

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - %{postgismajorversion}.3-5PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Tue Aug 18 2026 Devrim Gunduz <devrim@gunduz.org> - 3.6.3-4PGDG
- Build with GDAL 3.13 on all platforms except RHEL 8.

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 3.6.3-3PGDG
- Add Amazon Linux 2023 support.

* Mon Apr 27 2026 Devrim Gunduz <devrim@gunduz.org> - 3.6.3-2PGDG
- Update GDAL dependency for SLES 15.

* Thu Apr 16 2026 Devrim Gündüz <devrim@gunduz.org> - 3.6.3-1PGDG
- Update to 3.6.3 per:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.6.3/NEWS
- Build against PROJ 9.8 on all platforms except RHEL 8
- Strip -flto from generated Makefiles on RHEL 8 (breaks RHEL 8 static
  archive linking). Fixes https://github.com/pgdg-packaging/pgdg-rpms/issues/173

* Tue Feb 10 2026 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-1PGDG
- Update to 3.6.2 per:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.6.2/NEWS

* Mon Nov 17 2025 Devrim Gündüz <devrim@gunduz.org> - 3.6.1-1PGDG
- Update to 3.6.1 per:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.6.1/NEWS
- Build with GDAL 3.12 on all platforms except RHEL 8 and SLES 15.

* Wed Nov 12 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.0-6PGDG
- Fix pcre2 dependency on RHEL 8 and 9. Per report from Christopher Lorenz:
  https://www.postgresql.org/message-id/fc8e323142484d98b5d1720e0811ce9c%40ZIT-BB.Brandenburg.de

* Mon Nov 10 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.0-5PGDG
- Update pcre2 and libxerces dependencies on SLES.

* Tue Oct 7 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.0-4PGDG
- Rebuild against PROJ 9.7 on all platforms except RHEL 8

* Sun Oct 5 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.0-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 3.6.0-2PGDG.1
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Sep 23 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.0-1PGDG.1
- Rebuild for Fedora 43

* Tue Sep 2 2025 Devrim Gündüz <devrim@gunduz.org> - 3.6.0-1PGDG
- Update to 3.6.0 per:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.6.0/NEWS

* Tue Aug 26 2025 Devrim Gündüz <devrim@gunduz.org> - 3.6.0rc2-1PGDG
- Update to 3.6.0 rc2
- Rebuild against GeOS 3.14

* Sat Aug 23 2025 Devrim Gündüz <devrim@gunduz.org> - 3.6.0rc1-1PGDG
- Update to 3.6.0 rc1

* Thu Jul 31 2025 Devrim Gündüz <devrim@gunduz.org> - 3.6.0beta1-2PGDG
- Rebuild against GDAL 3.11.3

* Wed Jul 23 2025 Devrim Gündüz <devrim@gunduz.org> - 3.6.0beta1-1PGDG
- Update to 3.6.0 beta1

* Thu Jul 17 2025 Devrim Gündüz <devrim@gunduz.org> - 3.6.0alpha1-2PGDG
- Use GDAL 3.11 and PROJ 9.6 on RHEL 8 and SLES 15 as well.

* Sat Jul 5 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.0alpha1-1PGDG
- Initial cut for PostGIS 3.6.0 alpha1
