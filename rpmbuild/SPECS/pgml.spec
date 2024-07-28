%define debug_package %{nil}
%global pname pgml
%global sname postgresml
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{pname}_%{pgmajorversion}
Version:	2.9.2
Release:	1PIGSTY%{?dist}
Summary:	PostgresML is a complete MLOps platform in a PostgreSQL extension. Build simpler, faster and more scalable models right inside your database.
License:	MIT license
URL:		https://github.com/postgresml/postgresml
Requires:	postgresql%{pgmajorversion}-server

%description
PostgresML is a machine learning extension for PostgreSQL that enables you to perform training and inference on text and tabular data using SQL queries.
 With PostgresML, you can seamlessly integrate machine learning models into your PostgreSQL database and harness the power of cutting-edge algorithms to process data efficiently.

%install
%{__rm} -rf %{buildroot}
install -d %{buildroot}%{pginstdir}/lib/
install -d %{buildroot}%{pginstdir}/share/extension/
install -m 755 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 2.9.2
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 2.9.1
- Bump version to v2.9.1 with pgrx 0.11.3
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 2.8.1
- Bump version to v2.8.2 with PG 16 support
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 2.7.9
- Initial RPM release, used by Pigsty <https://pigsty.io>