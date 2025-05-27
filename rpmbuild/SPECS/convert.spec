%define debug_package %{nil}
%global pname convert
%global sname convert
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		pg_%{sname}_%{pgmajorversion}
Version:	0.0.4
Release:	1PIGSTY%{?dist}
Summary:	Postgres extension for common conversions when working with spatial data.
License:	MIT
URL:		https://github.com/rustprooflabs/%{pname}
SOURCE0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Convert is a Postgres extension providing common conversion functions, such as meters to feet or miles to kilometers.

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
* Tue May 27 2025 Vonng <rh@vonng.com> - 0.0.4
- Initial RPM release, pgrx 0.14.1, used by Pigsty <https://pigsty.io>