%global pname pgmnemo
%global sname pgmnemo
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17
%{error:pgmnemo 0.13.0 only supports PostgreSQL 17+}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.13.0
Release:	1PIGSTY%{?dist}
Summary:	Provenance-gated vector memory for LLM agents in PostgreSQL
License:	Apache-2.0
URL:		https://github.com/pgmnemo/pgmnemo
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgmnemo/0.13.0/pgmnemo-0.13.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	pgvector_%{pgmajorversion} >= 0.7.0

%description
pgmnemo provides a provenance-gated, vector-hybrid memory substrate for LLM
agents in PostgreSQL. It installs SQL schema objects and depends on pgvector.

%prep
%setup -q -n %{sname}-%{version}
cp -f extension/%{pname}.control %{pname}.control

%build
# SQL-only PGXS extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
%{__install} -m 644 extension/%{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun Jul 19 2026 Vonng <rh@vonng.com> - 0.13.0-1PIGSTY
- Update to upstream PGXN 0.13.0
- Follow upstream's new PostgreSQL 17+ runtime requirement

* Wed Jul 01 2026 Vonng <rh@vonng.com> - 0.12.1-1PIGSTY
- Update to upstream PGXN 0.12.1

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 0.8.3-1PIGSTY
- Update to upstream PGXN 0.8.3

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.7.2-1PIGSTY
- Initial RPM release for upstream PGXN 0.7.2
