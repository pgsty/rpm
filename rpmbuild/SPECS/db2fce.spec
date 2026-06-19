%define debug_package %{nil}
%global pname db2fce
%global sname db2fce
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:db2fce only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.17
Release:	1PIGSTY%{?dist}
Summary:	DB2 compatibility environment for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/credativ/db2fce
Source0:	%{sname}-%{version}.tar.gz
#           https://deb.debian.org/debian/pool/main/d/db2fce/db2fce_0.0.17.orig.tar.gz
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
db2fce provides DB2 compatibility functions, types, operators, and the
SYSIBM.SYSDUMMY1 view for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license COPYRIGHT.db2fce
%doc README.md NEWS META.json
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude %{pginstdir}/doc/extension/COPYRIGHT.db2fce

%changelog
* Fri Jun 19 2026 Vonng <rh@vonng.com> - 0.0.17-1PIGSTY
- Initial RPM release for upstream 0.0.17
