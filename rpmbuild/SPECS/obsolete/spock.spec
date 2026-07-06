%global sname spock
%global pname spock
%global pgmajorversion 18
%global pgkernelversion 18.3
%global pginstdir /usr/pgedge-%{pgmajorversion}

Name:           %{sname}_%{pgmajorversion}
Version:        5.0.6
Release:        1PIGSTY%{?dist}
Summary:        Spock multi-master replication extension for pgEdge PostgreSQL
License:        PostgreSQL
URL:            https://github.com/pgEdge/spock
Source0:        %{pname}-%{version}.tar.gz

BuildRequires:  pgedge_%{pgmajorversion} >= %{pgkernelversion}
BuildRequires:  jansson-devel, pkgconfig
Requires:       pgedge_%{pgmajorversion} >= %{pgkernelversion}

%description
Spock multi-master replication extension package for pgEdge PostgreSQL %{pgmajorversion}.

%prep
%setup -q -n %{pname}-%{version}

%build
export PATH=%{pginstdir}/bin:$PATH
export PG_CONFIG=%{pginstdir}/bin/pg_config
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin:$PATH
export PG_CONFIG=%{pginstdir}/bin/pg_config
USE_PGXS=1 %{__make} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/postgresql/spock*.so
%{pginstdir}/share/postgresql/extension/spock.control
%{pginstdir}/share/postgresql/extension/spock*.sql
%{pginstdir}/bin/spockctrl
%{pginstdir}/share/postgresql/spock
%exclude %{pginstdir}/lib/postgresql/bitcode/*
%exclude /usr/lib/.build-id/*

%changelog
* Fri May 01 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 5.0.6-1PIGSTY
- Build Spock extension against pgedge_18 using PGXS

* Tue Feb 24 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 5.0.5-1PIGSTY
- Build Spock extension against pgedge_17 using PGXS
