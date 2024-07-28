%define debug_package %{nil}
%global pname pgjwt
%global sname pgjwt
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL implementation of JSON Web Tokens
License:	MIT
URL:		https://github.com/michelp/%{sname}
Source0:	https://github.com/michelp/%{sname}/archive/refs/tags/pgjwt-0.2.0.tar.gz
#           https://github.com/michelp/pgjwt/archive/refs/heads/master.zip
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL implementation of JSON Web Tokens, pure SQL

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 0.2.0
- Initial RPM release, used by Pigsty <https://pigsty.io>