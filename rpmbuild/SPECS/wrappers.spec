%define debug_package %{nil}
%global pname wrappers
%global sname wrappers
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.4.1
Release:	1PIGSTY%{?dist}
Summary:	Postgres Foreign Data Wrappers by Supabase
License:	Apache-2.0
URL:		https://github.com/supabase/wrappers
#           https://github.com/supabase/wrappers/archive/refs/tags/v0.4.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Wrappers is a development framework for Postgres Foreign Data Wrappers (FDW), written in Rust.
Its goal is to make Postgres FDW development easier while keeping Rust language's modern capabilities,
such as high performance, strong types, and safety.
HelloWorld, BigQuery, Clickhouse, Stripe, Firebase, Airtable, S3, Logflare, Auth0, SQL, Redis, AWS Cognito, Notion, Snowflake, Paddle


%install
%{__rm} -rf %{buildroot}
install -d %{buildroot}%{pginstdir}/lib/
install -d %{buildroot}%{pginstdir}/share/extension/
install -m 755 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}-%{version}.so %{buildroot}%{pginstdir}/lib/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}-*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.4.1
* Sun May 5 2024 Vonng <rh@vonng.com> - 0.3.1
- Initial RPM release, used by Pigsty <https://pigsty.io>