%define debug_package %{nil}
%global pname timescaledb_toolkit
%global sname timescaledb-toolkit
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.22.0
Release:	1PIGSTY%{?dist}
Summary:	Extension for more hyperfunctions, fully compatible with TimescaleDB and PostgreSQL
License:	Timescale
URL:		https://github.com/timescale/timescaledb-toolkit
SOURCE0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Recommends: pg_cron_%{pgmajorversion}

%description
Extension for more hyperfunctions, fully compatible with TimescaleDB and PostgreSQL

%prep
%setup -q -n %{sname}-%{version}

%build
cd extension
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
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 1.22.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 1.21.0-1PIGSTY
* Thu Jan 23 2025 Vonng <rh@vonng.com> - 1.19.0-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>