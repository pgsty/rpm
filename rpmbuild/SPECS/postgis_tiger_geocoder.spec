%global pname postgis_tiger_geocoder
%global sname postgis_tiger_geocoder
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:postgis_tiger_geocoder is packaged for PostgreSQL 16 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2025.2
Release:        1PGSTY%{?dist}
Summary:        PostGIS Tiger geocoder and reverse geocoder
License:        GPL-2.0-only
URL:            https://gitea.osgeo.org/postgis/postgis_tiger_geocoder
Source0:        %{sname}-%{version}.tar.gz
# https://gitea.osgeo.org/postgis/postgis_tiger_geocoder/releases/download/2025.2/postgis_tiger_geocoder-2025.2.tar.gz

BuildRequires:  postgresql%{pgmajorversion}
BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  make

Requires:       postgresql%{pgmajorversion}
Requires:       postgis3_%{pgmajorversion} >= 3.7.0
BuildArch:      noarch

%description
The postgis_tiger_geocoder is a PL/pgSQL extension that provides functions
for geocoding, reverse geocoding, and standardizing address data using US
Census TIGER/Line data. It also includes helper functions for loading the
TIGER data into PostgreSQL.

%prep
%setup -q -n %{sname}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%license COPYING
%doc SECURITY.md
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*

%changelog
* Thu Nov 05 2026 Ruohang Feng <rh@vonng.com> - 2025.2-1PGSTY
- Declare the make build dependency for the standalone SQL package.

* Mon Nov 02 2026 Ruohang Feng <rh@vonng.com> - 2025.2-1PGSTY
- Package the PostGIS Tiger geocoder independently following the PostGIS 3.7 split.
- Restrict the package to PostgreSQL 16 through 18, matching upstream support.
- Match the GPL-2 license in the upstream archive.
