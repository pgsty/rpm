%define debug_package %{nil}
%global pname schedoc
%global sname pg_schedoc
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	1PGSTY%{?dist}
Summary:	Cross documentation between Django and DBT projects
License:	GPL-3.0-only
URL:		https://github.com/ZeroGachis/pg_schedoc
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server ddl_historization_%{pgmajorversion}

%description
schedoc generates schema documentation from COMMENT metadata on PostgreSQL
objects. It requires the ddl_historization extension. Column comments use a
JSON format with predefined values such as status.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
