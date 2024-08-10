%define debug_package %{nil}
%global pname meta
%global sname pg_meta
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.4.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Extension: More friendly system catalog for PostgreSQL
License:	BSD-2
URL:		https://github.com/aquameta/meta
Source0:	meta-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Meta System catalog: ~30 views (full list) that, under the hood, query and synthesize pg_catalog and information_schema
Meta-identifiers: A set of composite types that encapsulate variables necessary to identify PostgreSQL objects (tables, columns, casts, types, etc.) by name, and serve as "soft" primary keys to the views above. See meta-identifiers for more.
Catalog triggers: Optional meta_triggers extension, which adds INSERT/UPDATE triggers on the catalog's views. These triggers make it possible to do DDL statements (e.g. CREATE TABLE ...) with an DML statement (e.g. insert into meta.table (name) values('foo')), similar to a schema diff and migration tool but with a data-centric approach.


%prep
%setup -q -n meta-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
#%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.4.0
- Initial RPM release, used by Pigsty <https://pigsty.io>