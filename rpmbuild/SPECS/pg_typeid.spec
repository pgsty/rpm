%define debug_package %{nil}
%global pname typeid
%global sname pg_typeid
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.0
Release:	1PIGSTY%{?dist}
Summary:	TypeID support for PostgreSQL
License:	MIT
URL:		https://github.com/blitss/typeid-postgres
Source0:	typeid-postgres-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
typeid-postgres enables native support for TypeIDs in PostgreSQL. TypeIDs are a modern
alternative to UUIDs based on UUIDv7, providing a human-readable prefix and a sortable
UUID suffix encoded in base32. This extension brings type-safe, sortable, and prefixed
unique identifiers to PostgreSQL, ideal for distributed systems and modern applications.

%prep
%setup -q -n typeid-postgres-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/typeid-postgres-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/typeid-postgres-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/typeid-postgres-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sun Nov 17 2025 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>