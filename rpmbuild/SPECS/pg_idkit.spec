%define debug_package %{nil}
%global pname pg_idkit
%global sname pg_idkit
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.1
Release:	2PIGSTY%{?dist}
Summary:	pg_idkit is a Postgres extension for generating many popular types of identifiers
License:	Apache-2.0
URL:		https://github.com/Vonng/pg_idkit
SOURCE0:    pg_idkit-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_idkit is a Postgres extension for generating many popular types of identifiers:
uuidv6, uuidv7, nanoid, ksuid, ulid, timeflake, pushid, xid, cuid, cuid2

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
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.3.1-2PIGSTY
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 0.3.1-1PIGSTY
* Mon May 26 2025 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.2.4-1PIGSTY
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.2.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>