%define debug_package %{nil}
%global pname omnigres
%global sname omnigres
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	20250120
Release:	1PIGSTY%{?dist}
Summary:	Postgres as a Platform
License:	Apache-2.0
URL:		https://github.com/omnigres/omnigres
Source0:	omnigres-%{version}.tar.gz
BuildRequires:	pgdg-srpm-macros >= 1.0.27 cmake postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}-contrib postgresql%{pgmajorversion}-plpython3 cpan python3.11-devel python3.11-pyparsing python3.11-pip
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib postgresql%{pgmajorversion}-plpython3

%description
Omnigres makes Postgres a developer-first application platform.
You can deploy a single database instance and it can host your entire application, scaling as needed.

%prep
%setup -q -n %{sname}-%{version}

%build
cmake -S . -B pg%{pgmajorversion} -DCMAKE_BUILD_TYPE=Release -DOPENSSL_CONFIGURED=1 -DPython3_EXECUTABLE=/usr/bin/python3.11 -DPG_CONFIG=/usr/pgsql-%{pgmajorversion}/bin/pg_config;
cmake --build pg%{pgmajorversion} --parallel;
cmake --build pg%{pgmajorversion} --parallel --target package_extensions;

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/pg%{pgmajorversion}/packaged/*.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/pg%{pgmajorversion}/packaged/extension/* %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql
%exclude /usr/lib/.build-id

%changelog
* Mon Jan 20 2025 Vonng <rh@vonng.com> - 20250120
- Initial RPM release, used by Pigsty <https://pigsty.io>