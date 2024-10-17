%define debug_package %{nil}
%global pname pg_jsonschema
%global sname pg_jsonschema
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.3
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension providing JSON Schema validation
License:	Apache-2.0
URL:		https://github.com/supabase/pg_jsonschema
SOURCE0:    pg_jsonschema-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_jsonschema is a PostgreSQL extension adding support for JSON schema validation on json and jsonb data types.

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
* Thu Oct 17 2024 Vonng <rh@vonng.com> - 0.3.3
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.3.2
* Sun May 5 2024 Vonng <rh@vonng.com> - 0.3.1
- Initial RPM release, used by Pigsty <https://pigsty.io>