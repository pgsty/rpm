%global sname jev
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 17
%{error:jev supports PostgreSQL 14-17}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.2.0
Release:        1PGSTY%{?dist}
Summary:        Natural-language row predicates using the TypeSafe API
License:        PostgreSQL
URL:            https://github.com/realZachi/pg-jev
Source0:        %{sname}-%{version}.tar.gz
# PGXN ZIP normalized with GNU tar; see the corresponding DEB README.
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-plpython3

%description
jev filters, ranks and classifies PostgreSQL rows through a remote
TypeSafe model API. It requires plpython3u and an API key; row contents
are sent to the configured external service. This package contains SQL
and embedded Python code only, with no native shared library.

%prep
%setup -q -n jev-0.2.0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DOCS=

%install
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} DOCS=

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.2.0-1PGSTY
- Package upstream 0.2.0 for PostgreSQL 14 through 17
