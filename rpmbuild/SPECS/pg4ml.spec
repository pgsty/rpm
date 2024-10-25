%define debug_package %{nil}
%global pname pg4ml
%global sname pg4ml
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	2.0
Release:	1PIGSTY%{?dist}
Summary:	Machine Learning Framework for PostgreSQL
License:	AGPLv3
URL:		https://gitee.com/guotiecheng/plpgsql_pg4ml
Source0:	pg4ml-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Machine Learning Framework for PostgreSQL

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1  PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1  PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Oct 25 2023 Vonng <rh@vonng.com> - 2.0
- Initial RPM release, used by Pigsty <https://pigsty.io>