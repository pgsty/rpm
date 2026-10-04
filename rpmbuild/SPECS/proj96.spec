# Based on the PGDG EL8 source RPM; see bin/postgis-sources.json.
%global	_vpath_builddir .
%global sname proj

%pgdg_set_gis_variables

Name:		%{sname}96
Version:	9.6.2
Release:	1PGSTY%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	https://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	sqlite-devel >= 3.7 libcurl-devel cmake >= 3.16 sqlite
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.48

# Default GCC version on SLES 15 is not sufficient to build PROJ 9.4,
# so use a newer one:
%if 0%{?suse_version} >= 1500
BuildRequires:	gcc12-c++
%else
# The rest is safe:
BuildRequires:	gcc-c++
%endif

%if 0%{?suse_version} >= 1500
# Unfortunately SLES 15 ships the libraries with -devel subpackage:
Requires:	sqlite3-devel >= 3.7
%else
# All other sane distributions have a separate -libs subpackage:
Requires:	sqlite-libs >= 3.7
%endif


%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}

%description
PROJ is a generic coordinate transformation software that transforms
geospatial coordinates from one coordinate reference system (CRS) to another.
This includes cartographic projections as well as geodetic transformations.

%description devel
This package contains libproj and the appropriate header files and man pages.

%prep
%setup -q -n %{sname}-%{version}

%build
%set_build_flags

%{__install} -d build
pushd build

%if 0%{?suse_version} >= 1500
export CXX=/usr/bin/g++-12
%endif

%if 0%{?suse_version} >= 1500
cmake ..\
%else
cmake3 .. \
%endif
	-DCMAKE_INSTALL_PREFIX:PATH=%{proj96instdir} \
	-DCMAKE_EXE_LINKER_FLAGS="${LDFLAGS}" \
	-DCMAKE_SHARED_LINKER_FLAGS="${LDFLAGS}" \
	-DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
	-DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}"

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}
popd

%install
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}
popd

%{__install} -d %{buildroot}%{proj96instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj96instdir}/share/doc/
%{__install} -p -m 0644 NEWS.md AUTHORS.md COPYING README.md ChangeLog %{buildroot}%{proj96instdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{proj96instdir}/share/doc/*
%{proj96instdir}/share/bash-completion/completions/projinfo
%{proj96instdir}/bin/*
%{proj96instdir}/share/man/man1/*.1
%{proj96instdir}/share/proj/*
%{proj96instdir}/lib64/libproj.so.25*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj96instdir}/share/man/man1/*.1
%{proj96instdir}/include/*.h
%{proj96instdir}/include/proj/*
%{proj96instdir}/lib64/*.so
%attr(0755,root,root) %{proj96instdir}/lib64/pkgconfig/%{sname}.pc
%{proj96instdir}/lib64/cmake/%{sname}/*cmake
%{proj96instdir}/lib64/cmake/%{sname}4/*cmake

%changelog
* Sun Oct 04 2026 Ruohang Feng <rh@vonng.com> - 0:9.6.2-1PGSTY
- Import the PGDG EL8 branch with complete build flags and debug packages.
- Retain the upstream origin-relative RPATH.

* Fri Jun 6 2025 Devrim Gündüz <devrim@gunduz.org> - 0:9.6.2-1PGDG
- Update to 9.6.2 per changes described at:
  https://github.com/OSGeo/PROJ/releases/tag/9.6.2

* Mon Jun 2 2025 Devrim Gündüz <devrim@gunduz.org> - 0:9.6.1-1PGDG
- Update to 9.6.1

* Wed Apr 2 2025 Devrim Gündüz <devrim@gunduz.org> - 0:9.6.0-1PGDG
- Initial 9.6 packaging for PostgreSQL RPM Repository.
