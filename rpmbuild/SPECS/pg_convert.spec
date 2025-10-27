%define debug_package %{nil}
%global pname convert
%global sname pg_convert
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.4
Release:	2PIGSTY%{?dist}
Summary:	Postgres extension for common conversions when working with spatial data.
License:	MIT
URL:		https://github.com/Vonng/%{pname}
SOURCE0:    %{pname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Convert is a Postgres extension providing common conversion functions, such as meters to feet or miles to kilometers.

%prep
%setup -q -n %{pname}-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.0.4-2PIGSTY
* Tue May 27 2025 Vonng <rh@vonng.com> - 0.0.4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>