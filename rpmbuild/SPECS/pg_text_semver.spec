%global pname pg_text_semver
%global sname pg_text_semver
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.1
Release:	1PIGSTY%{?dist}
Summary:	Semantic version domain and comparison operators for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/bigsmoke/pg_text_semver
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/bigsmoke/pg_text_semver/archive/refs/tags/v1.2.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_text_semver provides a semver domain based on PostgreSQL text plus parsing,
comparison functions, casts, and operators for working with Semantic
Versioning 2.0.0 values inside SQL.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENCE.txt
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.2.1-1PIGSTY
- Initial RPM release based on upstream tag v1.2.1
