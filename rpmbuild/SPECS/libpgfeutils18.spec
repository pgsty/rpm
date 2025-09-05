%define debug_package %{nil}
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

%global pname postgresql
%global sname postgresql
%global pginstdir /usr/pgsql-18

Name:		libpgfeutils18
Version:	18rc1
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Front-End Utils Library
License:	PostgreSQL
URL:		https://www.postgresql.org
Source0:	postgresql-18rc1.tar.gz

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
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 18rc1-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>