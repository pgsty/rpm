%define debug_package %{nil}
%global pname pg_polyline
%global sname pg_polyline
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	2PIGSTY%{?dist}
Summary:	Fast Google Encoded Polyline encoding & decoding for postgres Extension
License:	MIT
URL:		https://github.com/yihong0618/pg_polyline
Source0:	pg_polyline-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Fast Google Encoded Polyline encoding & decoding for postgres Extension

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
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.0.1-2PIGSTY
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
* Sat Oct 19 2024 Vonng <rh@vonng.com> - 0.0.0-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>