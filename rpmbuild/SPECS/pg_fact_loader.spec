%global pname pg_fact_loader
%global sname pg_fact_loader
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:pg_fact_loader only supports PostgreSQL 15 through 19 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.1
Release:	1PGSTY%{?dist}
Summary:	Build and maintain fact tables asynchronously
License:	MIT
URL:		https://github.com/enova/pg_fact_loader
Source0:	%{sname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Maintain PostgreSQL fact tables using queue tables and worker functions.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Tue Nov 24 2026 Ruohang Feng <rh@vonng.com> - 2.0.1-1PGSTY
- Package the SQL extension for missing PGDG coordinates.
