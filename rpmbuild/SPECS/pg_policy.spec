%define debug_package %{nil}
%global pname pg_policy
%global sname pg_policy
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_policy only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PGSTY%{?dist}
Summary:	Agent policy language for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/rahiakil/pg-policy
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_policy/0.1.0/pg_policy-0.1.0.zip
Patch0:		pg-policy-0.1.0.patch
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_policy is a pure SQL and PL/pgSQL extension that stores and evaluates
agent-oriented guardrails, guidance policies, session events, and decision
logs. It complements PostgreSQL row-level security rather than replacing it.
The extension API is installed in the policy schema because PostgreSQL
reserves schema names beginning with pg_.

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
# Pure SQL and PL/pgSQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config DOCS=

%files
%license LICENSE
%doc README.md doc/pg_policy.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Wed Aug 12 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Add RPM package for upstream PGXN 0.1.0 and PostgreSQL 14 through 18
- Repair the upstream schema, reserved function name, and API search path
