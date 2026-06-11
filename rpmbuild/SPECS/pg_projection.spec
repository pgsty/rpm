%global pname pg_projection
%global sname pg_projection
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_projection only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	MongoDB-like read projections for JSONB in PostgreSQL
License:	MIT
URL:		https://github.com/suissa/pg_projection
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_projection/1.0.0/pg_projection-1.0.0.zip
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_projection adds MongoDB-style projection helpers for JSONB documents,
including single-document and query-result projection functions.

%prep
%setup -q -n %{sname}-%{version}

%build
# Pure SQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
install -m 0644 %{pname}.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 %{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun May 24 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.0
