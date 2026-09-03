%global pname pdu
%global sname pdu
%global pduver 3.0.25.12
%global commit 345422fa69adfb98cc2a33c65682edbdd3de851a
%global gitdate 20260822
%global shortcommit 345422f
%global buildsrc PDU-PostgreSQLDataUnloader-%{commit}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:PDU supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	%{pduver}
Release:	2.git%{gitdate}.%{shortcommit}PGSTY%{?dist}
Summary:	PostgreSQL data recovery and extraction utility
License:	Apache-2.0 AND PostgreSQL
URL:		https://github.com/wublabdubdub/PDU-PostgreSQLDataUnloader
Source0:	%{sname}-%{version}+git%{gitdate}.%{shortcommit}.tar.gz
#           https://github.com/wublabdubdub/PDU-PostgreSQLDataUnloader
Patch0:		pdu-3.0.25.12.patch

BuildRequires:	gcc make lz4-devel zlib-devel
Requires:	postgresql%{pgmajorversion}-server

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
patch -d %{buildsrc} -p1 --fuzz=0 < %{PATCH0}
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
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 3.0.25.12-2.git20260822.345422fPGSTY
- Update to upstream main snapshot 345422f without changing PDUVERSION
- Include recovery, boundary-check, and legacy metadata terminator fixes
- Bound metadata serialization to the actual stack buffer size

* Sat Mar 21 2026 Vonng <rh@vonng.com> - 3.0.25.12-1PIGSTY
- Initial RPM release for version-bound PDU binaries under %%{pginstdir}/bin
- Require the matching PostgreSQL server package for the versioned install root
