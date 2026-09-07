%global pname schedoc
%global sname pg_schedoc
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global source_commit 9f135c3427415c61771bbe69dc1cffbb999239f4
%global source_date 20260430
%global source_short 9f135c3

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_schedoc supports PostgreSQL 14 through 18 in Pigsty}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.2
Release:	1.git%{source_date}.%{source_short}PGSTY%{?dist}
Summary:	Cross documentation between Django and DBT projects
License:	GPL-3.0-only
URL:		https://github.com/ZeroGachis/pg_schedoc
Source0:	%{sname}-%{version}+git%{source_date}.%{source_short}.tar.gz
Patch0:		pg_schedoc-0.0.2.patch
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	ddl_historization_%{pgmajorversion} >= 0.0.8

%description
schedoc generates schema documentation from COMMENT metadata on PostgreSQL
objects. It requires the ddl_historization extension. Column comments use a
JSON format with predefined values such as status.

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
# Rebuild only generated inputs; retain the audited upgrade migration.
rm -f exclude.sql dist/schedoc--%{version}.sql
LC_ALL=C PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
LC_ALL=C PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 0.0.2-1.git20260430.9f135c3PGSTY
- Pin upstream develop snapshot 9f135c3
- Add the audited 0.0.1 to 0.0.2 migration
- Fix non-public same-schema calls and PostgreSQL 14 JSON validation
- Regenerate installation SQL with a deterministic exclusion-template order

* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
