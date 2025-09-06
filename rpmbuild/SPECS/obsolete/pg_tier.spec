%define debug_package %{nil}
%global pname pg_tier
%global sname pg_tier
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.4
Release:	1PIGSTY%{?dist}
Summary:	Postgres Extension to enable data tiering to AWS S3
License:	Apache-2.0
URL:		https://github.com/tembo-io/pg_tier
SOURCE0:    pg_tier-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Recommends: parquet_s3_fdw_%{pgmajorversion}

%description
A Postgres extension to tier data to external storage
Postgres Extension written in Rust, to enable data tiering to AWS S3

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
%exclude /usr/lib/.build-id

%changelog
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 0.0.4
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.0.3
- Initial RPM release, used by Pigsty <https://pigsty.io>