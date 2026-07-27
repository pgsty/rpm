%define debug_package %{nil}
%global pname qdgc
%global sname qdgc
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:qdgc only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Extended Quarter Degree Grid Cell codes for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/ragnvald/qdgc
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/qdgc/0.1.0/qdgc-0.1.0.zip
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
qdgc implements Extended Quarter Degree Grid Cell encoding, decoding, and
navigation in pure SQL. The same package also includes the optional
qdgc_postgis extension, which is usable when PostGIS is installed.

%prep
%setup -q -n %{sname}-%{version}

%build
# Pure SQL PGXS extensions, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}_postgis.control
%{pginstdir}/share/extension/%{pname}_postgis--*.sql

%changelog
* Mon Jul 27 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Add RPM package for upstream PGXN 0.1.0
