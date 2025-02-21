%define debug_package %{nil}
%global pname vchord_bm25
%global sname vchord_bm25
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.1
Release:	1PIGSTY%{?dist}
Summary:	Native BM25 Ranking Index in PostgreSQL
License:	AGPL-3.0
URL:		https://github.com/tensorchord/VectorChord-bm25
Source0:	VectorChord-bm25-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pgvector_%{pgmajorversion} >= 0.7.0

%description
A PostgreSQL extension for bm25 ranking algorithm.
We implemented the Block-WeakAnd Algorithms for BM25 ranking inside PostgreSQL.
This extension is currently in alpha stage and not recommended for production use.
We're still iterating on the tokenizer API to support more configurations and languages.
The interface may change in the future.

%prep
%setup -q -n VectorChord-bm25-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/VectorChord-bm25-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/VectorChord-bm25-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/VectorChord-bm25-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.1.1
* Mon Feb 10 2025 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>