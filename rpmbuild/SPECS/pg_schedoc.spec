%define debug_package %{nil}
%global pname schedoc
%global sname pg_schedoc
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	1PIGSTY%{?dist}
Summary:	Cross documentation between Django and DBT projects
License:	GPL-3.0
URL:		https://github.com/bigsmoke/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server ddl_historization_%{pgmajorversion}

%description
schedoc means schema documentation, it's a tool to build an automatic documentation
based on COMMENT on PostgresSQL objects. schedoc require the extension (ddl_historization to work）
COMMENT are set on columns in a json format with predefined values like status.

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
- Initial RPM release, used by Pigsty <https://pigsty.io>
