%define debug_package %{nil}
%global pname mysqlcompat
%global sname mysqlcompat
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.7
Release:	1PIGSTY%{?dist}
Summary:	MySQL compatibility functions
License:	unrestricted
URL:		https://github.com/2ndQuadrant/mysqlcompat
Source0:	mysqlcompat-%{version}.tar.gz
#           https://github.com/michelp/mysqlcompat/archive/refs/heads/master.zip
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
A reimplemenation of as many MySQL functions as possible in PostgreSQL, as an aid to porting

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
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 0.0.7
- Initial RPM release, used by Pigsty <https://pigsty.io>