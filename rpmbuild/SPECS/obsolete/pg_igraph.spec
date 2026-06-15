# Deferred in PGSTY RPM builds: keep the draft recipe for traceability, but do
# not include pg_igraph in active build targets until the graph stack is ready.
%global pname pg_igraph
%global sname pg_igraph
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_igraph only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PIGSTY%{?dist}
Summary:	Native graph traversal engine for PostgreSQL
License:	MIT
URL:		https://github.com/ineron/pg_igraph
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_igraph/1.1.0/pg_igraph-1.1.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc make flex bison
BuildRequires:	pg_ilib_%{pgmajorversion} >= 1.0
Requires:	postgresql%{pgmajorversion}-server
Requires:	pg_ilib_%{pgmajorversion} >= 1.0

%description
pg_igraph is a native PostgreSQL extension that adds graph traversal
capabilities, including BFS, shortest-path queries, Cypher-like syntax,
JSON parameters, and multi-graph support.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md README_PGXN.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id
%exclude /usr/lib/.build-id/*
%exclude /usr/lib/.build-id/*/*

%changelog
* Sun Jun 14 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.1.0
