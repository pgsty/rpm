%define debug_package %{nil}
%global pname pg_session_jwt
%global sname pg_session_jwt
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	Postgres Extension for JWT Sessions
License:	Apache-2.0
URL:		https://github.com/neondatabase/pg_session_jwt
Source0:	pg_session_jwt-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_session_jwt is a PostgreSQL extension designed to handle authenticated sessions through a JWT.
This JWT is then verified against a JWK (JSON Web Key) to ensure its authenticity.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo update
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
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.2.0
- https://github.com/neondatabase/pg_session_jwt/releases/tag/v0.2.0
* Thu Oct 31 2024 Vonng <rh@vonng.com> - 0.1.2
- Initial RPM release, used by Pigsty <https://pigsty.io>