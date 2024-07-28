%define debug_package %{nil}
%global pname pg_analytics
%global sname pg_analytics
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.6.1
Release:	1PIGSTY%{?dist}
Summary:	Accelerates analytical query processing inside Postgres
License:	GNU Affero General Public License v3.0
URL:		https://github.com/paradedb/paradedb/tree/dev/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_analytics is an extension that accelerates analytical query processing inside Postgres.
The performance of analytical queries that leverage pg_analytics is comparable to the performance
of dedicated OLAP databases — without the need to extract, transform, and load (ETL) the data
from your Postgres instance into another system. The purpose of pg_analytics is to be a drop-in
solution for fast analytics in Postgres with zero ETL.

The primary dependencies are:
Apache Arrow for column-oriented memory format
Apache DataFusion for vectorized query execution with SIMD
Apache Parquet for persistence
Delta Lake as a storage framework with ACID properties
pgrx, the framework for creating Postgres extensions in Rust

%install
%{__rm} -rf %{buildroot}
install -d %{buildroot}%{pginstdir}/lib/
install -d %{buildroot}%{pginstdir}/share/extension/
install -m 755 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 0.6.1
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 0.5.6
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 0.5.3
- Initial RPM release, used by Pigsty <https://pigsty.io>