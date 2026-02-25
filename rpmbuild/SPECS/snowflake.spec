%global sname snowflake
%global pname snowflake
%global pgmajorversion 17
%global pgkernelversion 17.7
%global pginstdir /usr/pgedge-%{pgmajorversion}

Name:           %{sname}_%{pgmajorversion}
Version:        2.4
Release:        1PIGSTY%{?dist}
Summary:        Snowflake style IDs for pgEdge PostgreSQL
License:        PostgreSQL
URL:            https://github.com/pgEdge/snowflake
Source0:        %{pname}-%{version}.tar.gz

BuildRequires:  pgedge_%{pgmajorversion} >= %{pgkernelversion}
Requires:       pgedge_%{pgmajorversion} >= %{pgkernelversion}

%description
Snowflake extension package for pgEdge PostgreSQL %{pgmajorversion}.

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
%{pginstdir}/lib/postgresql/%{pname}.so
%{pginstdir}/share/postgresql/extension/%{pname}.control
%{pginstdir}/share/postgresql/extension/%{pname}*.sql
%{pginstdir}/lib/postgresql/bitcode/*
%exclude /usr/lib/.build-id/*

%changelog
* Tue Feb 24 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 2.4-1PIGSTY
- Build Snowflake extension against pgedge_17 using PGXS
