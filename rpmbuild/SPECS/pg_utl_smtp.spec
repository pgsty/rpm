%global sname pg_utl_smtp
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_utl_smtp supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL pg_utl_smtp package
License:        PostgreSQL
URL:            https://github.com/HexaCluster/pg_utl_smtp
Source0:        pg_utl_smtp-2.0.tar.gz
# https://github.com/HexaCluster/pg_utl_smtp/releases/tag/v2.0
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-plperl perl(IO::Socket::SSL)

%description
pg_utl_smtp built from the official upstream 2.0 source for PostgreSQL.

%prep
%setup -q -n pg_utl_smtp-2.0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make}   install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 2.0-1PGSTY
- Add the upstream 2.0 package for PostgreSQL 14 through 18
