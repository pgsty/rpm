%define debug_package %{nil}
%global pname pg_parquet
%global sname pg_parquet
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	Copy to/from Parquet in S3 from within PostgreSQL
License:	PostgreSQL
URL:		https://github.com/CrunchyData/pg_parquet
Source0:	pg_parquet-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_parquet is a PostgreSQL extension that allows you to read and write Parquet files, which are located in S3 or file system,
 from PostgreSQL via COPY TO/FROM commands. It depends on Apache Arrow project to read and write Parquet files and pgrx project to extend PostgreSQL's COPY command.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%license LICENSE
%exclude /usr/lib/.build-id

%changelog
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.3.0
- https://github.com/CrunchyData/pg_parquet/releases/tag/v0.3.0
* Wed Jan 08 2025 Vonng <rh@vonng.com> - 0.2.0
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.1.1
* Sat Oct 19 2024 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>