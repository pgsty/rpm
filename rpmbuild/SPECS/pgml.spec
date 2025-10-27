%define debug_package %{nil}
%global pname pgml
%global sname pgml
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{pname}_%{pgmajorversion}
Version:	2.10.0
Release:	1PIGSTY%{?dist}
Summary:	PostgresML is a complete MLOps platform in a PostgreSQL extension. Build simpler, faster and more scalable models right inside your database.
License:	MIT license
URL:		https://github.com/postgresml/postgresml
Source0:    pgml-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
# deps: yum install python3.11 python3.11-devel python3-virtualenv openssl openssl-devel cmake pkg-config libomp libomp-devel openblas* llvm llvm-devel lld openblas*

%description
PostgresML is a machine learning extension for PostgreSQL that enables you to perform training and inference on text and tabular data using SQL queries.
 With PostgresML, you can seamlessly integrate machine learning models into your PostgreSQL database and harness the power of cutting-edge algorithms to process data efficiently.

%prep
%setup -q -n %{pname}-%{version}
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo update

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Tue Jan 21 2025 Vonng <rh@vonng.com> - 2.10.0
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 2.9.3
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 2.9.2
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 2.9.1
- Bump version to v2.9.1 with pgrx 0.11.3
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 2.8.1
- Bump version to v2.8.2 with PG 16 support
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 2.7.9
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>