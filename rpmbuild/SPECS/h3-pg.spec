%global _vpath_builddir .
%global sname h3-pg
%global pginstdir /usr/pgsql-%{pgmajorversion}

Summary:	Uber's H3 Hexagonal Hierarchical Geospatial Indexing System in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	4.2.3
Release:	1PIGSTY%{?dist}
License:	Apache
URL:		https://github.com/zachasme/%{sname}
Source0:	%{sname}-%{version}.tar.gz
Patch0:		h3-pg-useosh3.patch
BuildRequires:	cmake >= 3.20 h3-devel >= 4.2.0-3
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion} h3 >= 4.2.0-3

%description
This library provides PostgreSQL bindings for the H3 Core Library.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
%{__install} -d build
pushd build
%cmake3 .. -DCMAKE_BUILD_TYPE=Release \
	-DPostgreSQL_CONFIG=%{pginstdir}/bin/pg_config
popd
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README.md
%{pginstdir}/lib/h3.so
%{pginstdir}/lib/h3_postgis.so
%{pginstdir}/share/extension/h3*.sql
%{pginstdir}/share/extension/h3.control
%{pginstdir}/share/extension/h3_postgis.control

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 4.2.3-1PIGSTY
- Rebuild EL8 x86_64 packages for PostgreSQL 17 and 18

* Tue Jun 24 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.3-1PGDG
- Update to 4.2.3
