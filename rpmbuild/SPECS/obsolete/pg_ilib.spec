# Deferred in PGSTY RPM builds: keep the draft recipe for traceability, but do
# not include pg_ilib in active build targets until pg_igraph packaging resumes.
%global pname pg_ilib
%global sname pg_ilib
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_commit 689b9835c34ed6028de4aee2fe572b5d36c1e69a

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_ilib only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.5
Release:	1PIGSTY%{?dist}
Summary:	Typed binary serialization helpers for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/ineron/pg_ilib
Source0:	%{sname}-%{version}.tar.gz
#           normalized from ineron/pg_ilib main snapshot 689b9835c34ed6028de4aee2fe572b5d36c1e69a

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc make gmp-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_ilib provides compact typed bytea serialization helpers and universal
value_to_jsonb decoding for PostgreSQL. It is required by pg_igraph.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}-pg15-build.patch

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id
%exclude /usr/lib/.build-id/*
%exclude /usr/lib/.build-id/*/*

%changelog
* Sun Jun 14 2026 Vonng <rh@vonng.com> - 1.5-1PIGSTY
- Initial RPM release for ineron/pg_ilib main snapshot %{snapshot_commit}
