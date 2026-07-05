%define debug_package %{nil}
%global pname pgsql_tweaks
%global sname pgsql_tweaks
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgsql_tweaks only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.5
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL functions and views for daily work
License:	PostgreSQL
URL:		https://codeberg.org/pgsql_tweaks/pgsql_tweaks
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgsql_tweaks/1.0.5/pgsql_tweaks-1.0.5.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pgsql_tweaks contains PostgreSQL functions and views supporting daily work.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL-only PGXS extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE.md
%doc README.md PGXNREADME.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Sun Jul 05 2026 Vonng <rh@vonng.com> - 1.0.5-1PIGSTY
- Update to upstream PGXN 1.0.5 using the normalized source tarball

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 1.0.3-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.3
