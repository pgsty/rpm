%global sname pg_profile
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_profile 4.15 supports PostgreSQL 14 through 18 in Pigsty}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        4.15
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL historic workload reports
License:        PostgreSQL
URL:            https://github.com/zubkov-andrei/pg_profile
Source0:        %{sname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-contrib

%description
pg_profile collects PostgreSQL workload snapshots and produces historic
resource-usage reports.  It requires the dblink and plpgsql extensions.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 \
    PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 \
    PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md doc/pg_profile.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 4.15-1PGSTY
- Initial Pigsty RPM package for signed upstream pg_profile 4.15
- Preserve the released 4.11 to 4.14 and 4.14 to 4.15 extension SQL chain
