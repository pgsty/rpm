%define debug_package %{nil}
%global pname pg_search
%global sname pg_search
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.8.6
Release:	1PIGSTY%{?dist}
Summary:	Full text search over SQL tables using the BM25 algorithm
License:	AGPLv3 license
URL:		https://github.com/paradedb/paradedb/
SOURCE0:    paradedb-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_search is a PostgreSQL extension that enables full text search over SQL tables using the BM25 algorithm,
the state-of-the-art ranking function for full text search.
It is built on top of Tantivy, the Rust-based alternative to Apache Lucene, using pgrx.

%prep
%setup -q -n paradedb-%{version}
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo update

%build
cd %{pname}
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/paradedb-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/paradedb-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/paradedb-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Jul 26 2024 Vonng <rh@vonng.com> - 0.8.6
* Mon Jul 22 2024 Vonng <rh@vonng.com> - 0.8.5
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.8.4
* Fri Jul 05 2024 Vonng <rh@vonng.com> - 0.8.2
* Sun Jun 30 2024 Vonng <rh@vonng.com> - 0.8.1
* Sat May 15 2024 Vonng <rh@vonng.com> - 0.7.0
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 0.6.1
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 0.5.6
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 0.5.3
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>