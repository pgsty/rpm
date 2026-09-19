%global sname pg_grammar_guard
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_grammar_guard supports PostgreSQL 14-18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.4.1
Release:        1PGSTY%{?dist}
Summary:        Catalog-derived grammars and schema drift checks
License:        PostgreSQL
URL:            https://github.com/Manuelreyesbravo/pg_grammar_guard
Source0:        %{sname}-%{version}.tar.gz
# PGXN ZIP normalized with GNU tar; see the corresponding DEB README.
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server
Requires:       pg_living_assertions_%{pgmajorversion} >= 0.4.2

%description
pg_grammar_guard builds GBNF grammars and JSON Schema from PostgreSQL
catalog identifiers and detects changes to approved grammar definitions.
It uses pg_living_assertions to store and check approved baselines.
Constraining identifiers does not establish query semantic correctness.

%prep
%setup -q -n pg_grammar_guard-0.4.1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DOCS=

%install
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} DOCS=

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.4.1-1PGSTY
- Package upstream 0.4.1 for PostgreSQL 14 through 18
