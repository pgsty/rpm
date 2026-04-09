%define debug_package %{nil}
%global pname pg_dispatch
%global sname pg_dispatch
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.5
Release:	1PIGSTY%{?dist}
Summary:	Asynchronous SQL dispatcher
License:	PostgreSQL
URL:		https://github.com/Snehil-Shah/pg_dispatch
Source0:	%{sname}-%{version}.zip
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	unzip
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib
Requires:	pg_cron_%{pgmajorversion}

%description
pg_dispatch is an asynchronous SQL dispatcher built on top of pg_cron.

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
cd %{_builddir}
unzip -q %{SOURCE0}

%build
cd %{_builddir}/%{sname}-%{version}
:

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{_docdir}/%{name}/README.md
%{_licensedir}/%{name}/LICENSE

%changelog
* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.1.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
