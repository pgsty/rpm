%define debug_package %{nil}
%global pname data_historization
%global sname data_historization
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PIGSTY%{?dist}
Summary:	PLPGSQL Script to historize data in partitionned table
License:	PostgreSQL
URL:		https://github.com/rodo/postgresql-data-historization
Source0:	postgresql-data-historization-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PLPGSQL Script to historize data in partitioned table

%prep
%setup -q -n postgresql-data-historization-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%license META.json
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>