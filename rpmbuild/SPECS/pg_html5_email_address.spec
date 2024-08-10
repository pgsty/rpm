%define debug_package %{nil}
%global pname pg_html5_email_address
%global sname pg_html5_email_address
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.3
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL email validation that is consistent with the HTML5 spec
License:	PostgreSQL
URL:		https://github.com/bigsmoke/pg_html5_email_address
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_html5_email_address is a tiny PostgreSQL extension that offers email address validation that is consistent with the <input type="email"> validation in HTML5.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.2.3
- Initial RPM release, used by Pigsty <https://pigsty.io>