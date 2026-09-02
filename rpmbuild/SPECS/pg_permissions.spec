%global sname pg_permissions
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_permissions supports PostgreSQL 14 through 18 in Pigsty}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.4.1
Release:        1PGSTY%{?dist}
Summary:        Review and reconcile PostgreSQL object permissions
License:        PostgreSQL
URL:            https://github.com/cybertec-postgresql/pg_permissions
Source0:        %{sname}-REL_1_4_1.tar.gz
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_permissions provides views for reviewing all database object privileges,
updatable views for granting or revoking them, and desired-state comparisons.

%prep
%setup -q -n %{sname}-REL_1_4_1

%build
# Pure SQL PGXS extension; there is nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}
%{__rm} -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE
%doc README.md README.pg_permissions CHANGELOG
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.4.1-1PGSTY
- Initial Pigsty RPM package for signed upstream pg_permissions 1.4.1
- Cover PostgreSQL 14 through 18 with the complete 1.0 to 1.4 SQL chain
