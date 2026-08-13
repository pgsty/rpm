%define debug_package %{nil}
%global pname emaj
%global sname emaj
%global rpmname e-maj
%global oldname emaj_%{pgmajorversion}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:emaj only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{rpmname}_%{pgmajorversion}
Version:	5.0.0
Release:	1PGSTY%{?dist}
Summary:	Table change logging and rollback extension for PostgreSQL
License:	GPL-3.0-or-later
URL:		https://github.com/dalibo/emaj
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/E-Maj/5.0.0/E-Maj-5.0.0.zip
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib
Requires:	perl-DBI perl-DBD-Pg
Provides:	%{oldname} = %{version}-%{release}
Obsoletes:	%{oldname} < %{version}-%{release}

%description
E-Maj logs table changes with triggers and can inspect or roll back those
changes at a named mark. It also ships client tools for statistics, rollback
monitoring, and parallel rollback execution.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL and client-script extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%attr(755,root,root) %{pginstdir}/bin/emaj*.pl
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/%{pname}/

%changelog
* Thu Jul 30 2026 Vonng <rh@vonng.com> - 5.0.0-2PIGSTY
- Align package name with PGDG and obsolete emaj_$v

* Mon Jul 27 2026 Vonng <rh@vonng.com> - 5.0.0-1PIGSTY
- Add RPM package for upstream PGXN 5.0.0
