%define debug_package %{nil}
%global pname pagevis
%global sname pagevis
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1
Release:	1PIGSTY%{?dist}
Summary:    PostgreSQL data page visualisation
License:	MIT
URL:		https://github.com/hollobon/pagevis
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
The pagevis PostgreSQL extension currently contains a single function, show_page,
which returns an ASCII-graphical representation of the contents of a PostgreSQL database page. It uses the pageinspect extension,
which must be installed first. You must be superuser to call show_page, as it uses the pageinspect get_raw_page function.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
#%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
#%exclude /usr/lib/.build-id/*
#%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>