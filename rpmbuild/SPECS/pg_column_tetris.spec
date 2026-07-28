%define debug_package %{nil}
%global pname pg_column_tetris
%global sname pg_column_tetris
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_column_tetris only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Enforce efficient PostgreSQL column alignment
License:	MIT
URL:		https://github.com/rogerwelin/pg_column_tetris
Source0:	%{sname}-%{version}.tar.gz
#           normalized from upstream commit e70f9867c63e932cdaf87b2d34b6504adad9ce12
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_column_tetris is a pure SQL and PL/pgSQL extension that detects avoidable
row padding caused by inefficient column ordering. It can warn about or reject
suboptimal CREATE TABLE statements and audit existing tables.

%prep
%setup -q -n %{sname}-%{version}

%build
# Pure SQL and PL/pgSQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Tue Jul 28 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Add RPM package for upstream 0.1.0 snapshot e70f986
