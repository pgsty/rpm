%global sname pg_statecharts
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_statecharts supports PostgreSQL 16 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        Hierarchical state machines inside PostgreSQL transactions
License:        MIT
URL:            https://github.com/kronor-io/statecharts
# Upstream release bundle with LICENSE from the matching PGXN distribution.
Source0:        %{sname}-%{version}.tar.gz
BuildArch:      noarch
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-contrib

%description
SQL and PL/pgSQL tables, types, triggers and functions for hierarchical and
parallel state machines. State transitions commit together with application
data. Requires ltree in the public schema; no preload or restart is needed.

%package -n pg_statecharts_dev_%{pgmajorversion}
Summary:        SCXML import and migration tooling for pg_statecharts
Requires:       %{name} = %{version}-%{release}

%description -n pg_statecharts_dev_%{pgmajorversion}
Optional development tooling for importing SCXML statecharts and generating
Sqitch migrations. Server file access requires additional PostgreSQL privileges.
The runtime extension does not require this package.

%prep
%setup -q -n %{sname}-%{version}

%build
# Pure SQL: the upstream installer concatenates its ordered SQL source files.
mkdir stage
DEST="$PWD/stage" ./install.sh --dev

%install
mkdir -p %{buildroot}%{pginstdir}/share/extension
install -m 644 stage/* %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/pg_statecharts.control
%{pginstdir}/share/extension/pg_statecharts--*.sql

%files -n pg_statecharts_dev_%{pgmajorversion}
%license LICENSE
%doc pg_statecharts_dev/README.md
%{pginstdir}/share/extension/pg_statecharts_dev.control
%{pginstdir}/share/extension/pg_statecharts_dev--*.sql

%changelog
* Fri Nov 06 2026 Ruohang Feng <rh@vonng.com> - 0.1.0-1PGSTY
- Package the runtime and optional development extension for PostgreSQL 16-18.
