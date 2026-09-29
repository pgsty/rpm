%global sname pg_living_assertions
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_living_assertions supports PostgreSQL 14-18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.5.1
Release:        1PGSTY%{?dist}
Summary:        Executable SQL assertions with recorded verification history
License:        PostgreSQL
URL:            https://github.com/Manuelreyesbravo/pg_living_assertions
Source0:        %{sname}-%{version}.tar.gz
# Upstream tag source: https://codeload.github.com/Manuelreyesbravo/pg_living_assertions/tar.gz/refs/tags/v0.5.1
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_living_assertions stores SQL checks, their results, verification times
and assertion replacement history. Checks run on demand in a read-only
subtransaction that is always rolled back. This is not a per-write SQL ASSERTION constraint.

%prep
%setup -q -n pg_living_assertions-0.5.1

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
* Tue Sep 29 2026 Vonng <rh@vonng.com> - 0.5.1-1PGSTY
- Update to upstream 0.5.1
- Describe the read-only subtransaction checks and retain upgrade scripts

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.4.2-1PGSTY
- Package upstream 0.4.2 for PostgreSQL 14 through 18
- Retain upstream SQL extension version 0.4.1 and all upgrade scripts
