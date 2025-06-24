%define debug_package %{nil}
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

%global pname postgresql
%global sname postgresql
%global pginstdir /usr/pgsql-17

Name:		libpgfeutils
Version:	17.5
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Front-End Utils Library
License:	PostgreSQL
URL:		https://www.postgresql.org
Source0:	%{sname}-%{version}.tar.gz

%description
Add /usr/pgsql-17/lib/libpgfeutils.a for extension building

%prep
%setup -q -n %{pname}-%{version}

%build
./configure --without-readline --without-zlib
make -C src/fe_utils

%install
mkdir -p %{buildroot}%{pginstdir}/lib
install -p -m 0644 src/fe_utils/libpgfeutils.a %{buildroot}%{pginstdir}/lib/libpgfeutils.a

%files
%{pginstdir}/lib/libpgfeutils.a

%changelog
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 17.5-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>