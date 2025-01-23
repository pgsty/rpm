%define debug_package %{nil}
%global pname pg_xenophile
%global sname pg_xenophile
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.8.3
Release:	1PIGSTY%{?dist}
Summary:	More than the bare necessities for PostgreSQL i18n and l10n.
License:	PostgreSQL
URL:		https://github.com/michelp/pg_xenophile
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_xenophile PostgreSQL extension bundles a bunch of data,
data structures and routines that you often end up needing
when working on an international project

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE.txt
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jan 23 2024 Vonng <rh@vonng.com> - 0.8.3
- Initial RPM release, used by Pigsty <https://pigsty.io>