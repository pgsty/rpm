%define debug_package %{nil}
%global pname pdu
%global sname pdu
%global pduver 3.0.25.12
%global buildsrc %{sname}-%{pduver}
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	%{pduver}
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL data recovery and extraction utility
License:	Apache-2.0 AND PostgreSQL
URL:		https://github.com/wublabdubdub/PDU-PostgreSQLDataUnloader
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/wublabdubdub/PDU-PostgreSQLDataUnloader

BuildRequires:	gcc make lz4-devel zlib-devel

%description
PDU (PostgreSQL Data Unloader) is a standalone disaster recovery and data
extraction utility for PostgreSQL data directories.

This package builds the binary for PostgreSQL %{pgmajorversion} and installs it
under %{pginstdir}/bin/pdu. The binary is version-bound to the PostgreSQL major
version encoded at build time and must match the target PGDATA version.

%prep
rm -rf %{buildsrc}
mkdir -p %{buildsrc}
tar -xf %{SOURCE0} --strip-components=1 -C %{buildsrc}
cp -f %{_specdir}/LICENSE-PostgreSQL %{buildsrc}/LICENSE-PostgreSQL

%build
cd %{buildsrc}
sed -ri 's/^#define PG_VERSION_NUM .*/#define PG_VERSION_NUM %{pgmajorversion}/' basic.h
%{__make} CC="%{__cc}"

%install
cd %{buildsrc}
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/bin
mkdir -p %{buildroot}%{pginstdir}/share/%{sname}
install -pm 0755 pdu %{buildroot}%{pginstdir}/bin/pdu
install -pm 0644 pdu.ini %{buildroot}%{pginstdir}/share/%{sname}/pdu.ini.example

%files
%license %{buildsrc}/LICENSE %{buildsrc}/LICENSE-PostgreSQL
%doc %{buildsrc}/README.md %{buildsrc}/NOTICE
%{pginstdir}/bin/pdu
%dir %{pginstdir}/share/%{sname}
%{pginstdir}/share/%{sname}/pdu.ini.example

%changelog
* Sat Mar 21 2026 Vonng <rh@vonng.com> - 3.0.25.12-1PIGSTY
- Initial RPM release for version-bound PDU binaries under %%{pginstdir}/bin
