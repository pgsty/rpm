%global pname postgresql
%global sname postgresql
%global pginstdir /usr/pgsql-17

Name:		libpgfeutils17
Version:	17.11
Release:	1PGSTY%{?dist}
# The payload is a static archive; keep its DWARF in the archive itself.
%global __brp_strip_static_archive %{nil}
%undefine _debugsource_packages
Summary:	PostgreSQL Front-End Utils Library
License:	PostgreSQL
URL:		https://www.postgresql.org
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	gcc, make, bison, flex, perl(FindBin)
BuildRequires:	libicu-devel

%description
Add /usr/pgsql-17/lib/libpgfeutils.a for extension building

%prep
%setup -q -n %{pname}-%{version}

%build
%set_build_flags
./configure --without-readline --without-zlib
make submake-generated-headers
make -C src/fe_utils

%install
mkdir -p %{buildroot}%{pginstdir}/lib
install -p -m 0644 src/fe_utils/libpgfeutils.a %{buildroot}%{pginstdir}/lib/libpgfeutils.a

%files
%{pginstdir}/lib/libpgfeutils.a

%changelog
* Sat Sep 05 2026 Vonng <rh@vonng.com> - 17.11-1PGSTY
- Rebuild from PostgreSQL 17.11 and retain static archive debug information
- Require the FindBin module without forcing a Perl module stream upgrade
- Declare the ICU development dependency used by configure

* Mon Jul 06 2026 Vonng <rh@vonng.com> - 17.10-1PIGSTY
- Rebuild libpgfeutils from PostgreSQL 17.10 source

* Fri Feb 27 2026 Vonng <rh@vonng.com> - 17.9-1PIGSTY
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 17.6-1PIGSTY
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 17.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
