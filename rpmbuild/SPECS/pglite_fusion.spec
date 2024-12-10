%define debug_package %{nil}
%global pname pglite_fusion
%global sname pglite-fusion
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{pname}_%{pgmajorversion}
Version:	0.0.3
Release:	1PIGSTY%{?dist}
Summary:	Embed an SQLite database in your PostgreSQL table. AKA multitenancy has been solved.
License:	MIT
URL:		https://github.com/frectonz/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Embed an SQLite database in your PostgreSQL table. AKA multitenancy has been solved.

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
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.0.3
- Initial RPM release, used by Pigsty <https://pigsty.io>