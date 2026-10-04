%global pname addressing_dictionary
%global sname addressing_dictionary
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:addressing_dictionary only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.1
Release:        1PGSTY%{?dist}
Summary:        Address-aware text search dictionaries for PostgreSQL
License:        MIT
URL:            https://github.com/pramsey/pgsql-addressing-dictionary
Source0:        addressing_dictionary-1.1-bf3590e038d8.tar.gz
# Source: https://codeload.github.com/pramsey/pgsql-addressing-dictionary/tar.gz/bf3590e038d820c8eb5c79135e5a78abf5fc9f2f
# SHA256: 304188fa5e4aa0e7c8ad8aa4caf000608a01c7b38abac4793122028475dc0c43
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
Address-aware text search dictionaries for PostgreSQL.

%prep
%setup -q -n pgsql-addressing-dictionary-bf3590e038d820c8eb5c79135e5a78abf5fc9f2f

%build
# This extension contains only SQL and documentation.

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE.md
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/tsearch_data/addressing_en.*
%{pginstdir}/share/tsearch_data/addressing_fr.*

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.1-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
