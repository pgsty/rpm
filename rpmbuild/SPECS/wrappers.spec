%define debug_package %{nil}
%global pname wrappers
%global sname wrappers
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.5.6
Release:	1PIGSTY%{?dist}
Summary:	Postgres Foreign Data Wrappers by Supabase
License:	Apache-2.0
URL:		https://github.com/supabase/wrappers
Source0:    wrappers-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Wrappers is a development framework for Postgres Foreign Data Wrappers (FDW), written in Rust.
Its goal is to make Postgres FDW development easier while keeping Rust language's modern capabilities,
such as high performance, strong types, and safety.
HelloWorld, BigQuery, Clickhouse, Stripe, Firebase, Airtable, S3, Logflare, Auth0, SQL, Redis, AWS Cognito, Notion, Snowflake, Paddle

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{pname}
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}-%{version}.so       %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Oct 29 2025 Vonng <rh@vonng.com> - 0.5.6-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.5.5-1PIGSTY
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 0.5.4-1PIGSTY
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 0.5.3-1PIGSTY
* Thu May 22 2025 Vonng <rh@vonng.com> - 0.5.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.4.6-1PIGSTY
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.4.5-1PIGSTY
* Wed Jan 08 2025 Vonng <rh@vonng.com> - 0.4.4-1PIGSTY
* Thu Oct 17 2024 Vonng <rh@vonng.com> - 0.4.3-1PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.4.2-1PIGSTY
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.4.1-1PIGSTY
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.3.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>