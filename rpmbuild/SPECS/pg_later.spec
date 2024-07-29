%define debug_package %{nil}
%global pname pg_later
%global sname pg_later
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.1
Release:	1PIGSTY%{?dist}
Summary:	Execute SQL now and get the results later.
License:	PostgreSQL
SOURCE0:    pg_later-%{version}.tar.gz
URL:		https://github.com/tembo-io/pg_later
#           https://github.com/tembo-io/pg_later/archive/refs/tags/v0.1.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pgmq_%{pgmajorversion} >= 1.1.1

%description
Execute SQL now and get the results later.

A postgres extension to execute queries asynchronously. Built on pgmq.

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
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 0.1.1
* Sun May 5 2024 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>