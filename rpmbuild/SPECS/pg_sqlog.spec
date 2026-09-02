%define debug_package %{nil}
%global pname pg_sqlog
%global sname pg_sqlog
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global source_commit b016539f6448c2d01a3aec5067b4f1fc2bebb9be
%global source_date 20241118
%global source_short b016539

Name:		%{sname}_%{pgmajorversion}
Version:	1.7
Release:	1.git%{source_date}.%{source_short}PGSTY%{?dist}
Summary:	Provide SQL interface to PostgreSQL logs
License:	BSD-3-Clause
URL:		https://github.com/kouber/pg_sqlog
Source0:	pg_sqlog-%{version}+git%{source_date}.%{source_short}.tar.gz
#           normalized upstream master snapshot b016539f6448c2d01a3aec5067b4f1fc2bebb9be
BuildArch:	noarch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
pg_sqlog allows to query a foreign table, pointing to a log, recorded in a CSV format.
It has special functions to extract the query duration of each query, as well as to group similar queries together.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.7-1.git20241118.b016539PGSTY
- Pin upstream master snapshot %{source_commit}
- Package the upstream 1.6 to 1.7 SQL upgrade path

* Thu Jul 18 2024 Vonng <rh@vonng.com> - 1.6
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
