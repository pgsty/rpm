%define debug_package %{nil}
%global pname pg_search
%global sname pg_search
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.21.2
Release:	1PIGSTY%{?dist}
Summary:	Full text search over SQL tables using the BM25 algorithm
License:	AGPL-3.0
URL:		https://github.com/paradedb/paradedb/
SOURCE0:    pg_search-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_search is a PostgreSQL extension that enables full text search over SQL tables using the BM25 algorithm,
the state-of-the-art ranking function for full text search.
It is built on top of Tantivy, the Rust-based alternative to Apache Lucene, using pgrx.

%prep
%setup -q -n pg_search-%{version}


%build
cd %{pname}
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo update
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 0.21.2-1PIGSTY
- bump to 0.21.2 with PG 15-18 support
* Wed Dec 24 2025 Vonng <rh@vonng.com> - 0.20.5-1PIGSTY
* Tue Dec 16 2025 Vonng <rh@vonng.com> - 0.20.4-1PIGSTY
* Mon Dec 15 2025 Vonng <rh@vonng.com> - 0.20.3-1PIGSTY
* Sat Nov 22 2025 Vonng <rh@vonng.com> - 0.20.0-1PIGSTY
* Tue Nov 18 2025 Vonng <rh@vonng.com> - 0.19.7-1PIGSTY
* Fri Jul 26 2024 Vonng <rh@vonng.com> - 0.8.6-1PIGSTY
* Mon Jul 22 2024 Vonng <rh@vonng.com> - 0.8.5-1PIGSTY
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.8.4-1PIGSTY
* Fri Jul 05 2024 Vonng <rh@vonng.com> - 0.8.2-1PIGSTY
* Sun Jun 30 2024 Vonng <rh@vonng.com> - 0.8.1-1PIGSTY
* Sat May 15 2024 Vonng <rh@vonng.com> - 0.7.0-1PIGSTY
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 0.6.1-1PIGSTY
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 0.5.6-1PIGSTY
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 0.5.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>