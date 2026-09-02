%define debug_package %{nil}
%global pname geoip
%global sname geoip
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global commit fcad7f1a42028b2c408e93d87e32580e1c991f80
%global gitdate 20250804
%global shortcommit fcad7f1

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:geoip supports PostgreSQL 14 through 18 in Pigsty}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.4.0
Release:	1.git%{gitdate}.%{shortcommit}PGSTY%{?dist}
Summary:	PostgreSQL extension for GeoIP geolocation

License:	BSD-2-Clause
URL:		https://github.com/tvondra/geoip
Source0:	geoip-%{version}+git%{gitdate}.%{shortcommit}.tar.gz

BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	ip4r_%{pgmajorversion}

%description
This extension provides IP-based geolocation, i.e. you provide an IPv4 address and the extension looks for info about country, city, GPS etc.
To operate, the extension needs data mapping IP addresses to the other info, but these data are not part of the extension. A good free dataset is GeoLite from MaxMind (available at www.maxmind.com).

%prep
%setup -q -n %{sname}-%{commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/*.sql

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.4.0-1.git20250804.fcad7f1PGSTY
- Update to upstream snapshot fcad7f1 with extension version 0.4.0
- Add the PostgreSQL 14 through 18 guard and explicit ip4r dependency

* Tue Jul 30 2024 Vonng <rh@vonng.com> - 0.3.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
