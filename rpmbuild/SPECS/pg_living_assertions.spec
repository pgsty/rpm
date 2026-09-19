%global sname pg_living_assertions
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_living_assertions supports PostgreSQL 14-18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.4.2
Release:        1PGSTY%{?dist}
Summary:        Executable SQL assertions with recorded verification history
License:        PostgreSQL
URL:            https://github.com/Manuelreyesbravo/pg_living_assertions
Source0:        %{sname}-%{version}.tar.gz
# PGXN ZIP normalized with GNU tar; see the corresponding DEB README.
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_living_assertions stores SQL checks, their results, verification times
and assertion replacement history. Checks run on demand in a read-only
STABLE context. This is not a per-write SQL ASSERTION constraint.
The distribution version is 0.4.2; the SQL extension version is 0.4.1.

%prep
%setup -q -n pg_living_assertions-0.4.2

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
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.4.2-1PGSTY
- Package upstream 0.4.2 for PostgreSQL 14 through 18
- Retain upstream SQL extension version 0.4.1 and all upgrade scripts
