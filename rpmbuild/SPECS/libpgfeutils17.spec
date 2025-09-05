%define debug_package %{nil}
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

%global pname postgresql
%global sname postgresql
%global pginstdir /usr/pgsql-17

Name:		libpgfeutils17
Version:	17.6
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Front-End Utils Library
License:	PostgreSQL
URL:		https://www.postgresql.org
Source0:	%{sname}-%{version}.tar.gz

BuildRequires: perl-FindBin

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
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 17.6-1PIGSTY
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 17.5-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>