%global sname pg_checksums
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_checksums supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.4
Release:        1PGSTY%{?dist}
Summary:        Check and manage PostgreSQL data checksums
License:        PostgreSQL
URL:            https://github.com/credativ/pg_checksums
Source0:        pg_checksums-1.4.tar.gz
# https://github.com/credativ/pg_checksums/releases/tag/1.4

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make
Requires:       postgresql%{pgmajorversion}-server

%description
The pg_checksums_ext utility checks, enables and disables PostgreSQL data checksums.

%prep
%setup -q -n pg_checksums-1.4

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make}   install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license COPYRIGHT
%doc README.md
%{pginstdir}/bin/pg_checksums_ext

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 1.4-1PGSTY
- Add the upstream 1.4 package for PostgreSQL 14 through 18
