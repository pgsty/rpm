%define debug_package %{nil}
%global pname geoip
%global sname geoip
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension for GeoIP geolocation

License:	BSD-Like
URL:		https://github.com/tvondra/geoip
Source0:	geoip-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
This extension provides IP-based geolocation, i.e. you provide an IPv4 address and the extension looks for info about country, city, GPS etc.
To operate, the extension needs data mapping IP addresses to the other info, but these data are not part of the extension. A good free dataset is GeoLite from MaxMind (available at www.maxmind.com).

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/*.sql

%changelog
* Tue Jul 30 2024 Vonng <rh@vonng.com> - 0.3.0
- Initial RPM release, used by Pigsty <https://pigsty.io>