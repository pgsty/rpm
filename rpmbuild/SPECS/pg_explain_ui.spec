%define debug_package %{nil}
%global pname explain_ui
%global sname pg_explain_ui
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	1PIGSTY%{?dist}
Summary:	A Postgres extension that allows you to easily jump into a visual plan UI for any SQL query,
License:	No License
URL:		https://github.com/davidgomes/pg-explain-ui
Source0:	pg_explain_ui-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
This is a simple Postgres extension that allows you to easily jump into a visual plan UI for any SQL query.

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
* Sat Oct 19 2024 Vonng <rh@vonng.com> - 0.0.1
- Initial RPM release, used by Pigsty <https://pigsty.io>