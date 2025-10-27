%define debug_package %{nil}
%global pname pg_upless
%global sname pg_upless
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.3
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Extension to Detect Useless UPDATE
License:	PostgreSQL
URL:		https://github.com/rodo/pg_upless
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_upless is a set of functions and tables, to build statistics on useless update statements.
With modern ORM it can occurs that sometimes an UPDATE is done without changing any values.
If it occurs too often that will impact the performance of your system.
pg_upless will help to detect them by creating triggers on the tables you want to follow.
It's not aimed to be used all the time, it's more a diagnostc tool you activate it a small period of time.
Even if it is designed to have the lower imapct as possible it will downgrade by a little your queries performance.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.0.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>