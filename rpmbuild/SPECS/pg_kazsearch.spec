%define debug_package %{nil}
%global pname pg_kazsearch
%global sname pg_kazsearch
%global srcdir pg-kazsearch-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_kazsearch supports PostgreSQL 16-18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.0
Release:	1PIGSTY%{?dist}
Summary:	Kazakh full-text search dictionary and stemmer for PostgreSQL
License:	LGPL-3.0
URL:		https://github.com/darkhanakh/pg-kazsearch
Source0:	%{sname}-%{version}.tar.gz
#           normalized from upstream release/tag https://github.com/darkhanakh/pg-kazsearch/releases/tag/v2.0.0

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang
Requires:	postgresql%{pgmajorversion}-server

%description
pg_kazsearch adds a Kazakh full-text search template, dictionary, stopword
list, and ready-to-use configuration for PostgreSQL. It implements a Rust
stemmer with lexicon-aware suffix stripping and ships the associated
tsearch_data payload for Kazakh search.

%prep
%setup -q -n %{srcdir}
# Upstream v2.0.0 still ships pg_ext/Cargo.toml with version 0.1.0.
# Normalize the pgrx-generated control/sql version to the packaged release.
sed -i -E '/^\[package\]/,/^\[/{s/^version = ".*"/version = "%{version}"/}' pg_ext/Cargo.toml

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch
# pgrx 0.17.0 uses NonNull::from_mut(), which is newer than the EL9 Rust
# shipped in our validation container. Rewriting to NonNull::from(&mut ...)
# preserves semantics and keeps the extension buildable on EL9A.
PBOX="$(find "$HOME/.cargo/registry/src" -path '*/pgrx-0.17.0/src/palloc/pbox.rs' | head -n 1)"
test -n "$PBOX"
if ! grep -q 'NonNull::from(\&mut datum)' "$PBOX"; then \
    (cd "$(dirname "$PBOX")" && patch -p0 < %{_specdir}/patches/pgrx-0.17.0-pbox-nonnull.patch); \
fi
cargo pgrx package -v -p %{pname} --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{pginstdir}/share/tsearch_data
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/data/tsearch_data/kaz_* %{buildroot}%{pginstdir}/share/tsearch_data/
install -m 644 %{_builddir}/%{srcdir}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/tsearch_data/kaz_stems.dict
%{pginstdir}/share/tsearch_data/kaz_stopwords.stop
%exclude /usr/lib/.build-id/*

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- Package upstream release v2.0.0 for PostgreSQL 16-18
- Normalize the pgrx-generated extension version to 2.0.0 during build
- Install the bundled Kazakh tsearch_data lexicon and stopword files
