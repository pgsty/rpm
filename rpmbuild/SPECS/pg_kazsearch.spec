%define debug_package %{nil}
%global pname pg_kazsearch
%global sname pg_kazsearch
%global srcdir darkhanakh-pg-kazsearch-c344ee9
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_kazsearch supports PostgreSQL 16-18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.2.0
Release:	1PIGSTY%{?dist}
Summary:	Kazakh full-text search dictionary and stemmer for PostgreSQL
License:	LGPL-3.0
URL:		https://github.com/darkhanakh/pg-kazsearch
Source0:	%{sname}-%{version}.tar.gz
#           normalized from upstream release/tag https://github.com/darkhanakh/pg-kazsearch/releases/tag/v2.2.0

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
# Normalize the pgrx-generated control/sql version to the packaged release.
sed -i -E '/^\[package\]/,/^\[/{s/^version = ".*"/version = "%{version}"/}' pg_ext/Cargo.toml
patch -p1 --forward -f < %{_specdir}/patches/pg-kazsearch-2.2.0.patch

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.18.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo update -p pgrx --precise $PGRX_VERSION
cargo update -p pgrx-tests --precise $PGRX_VERSION
cargo fetch

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
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
* Mon Jun 15 2026 Vonng <rh@vonng.com> - 2.2.0-1PIGSTY
- Package upstream release 2.2.0 for PostgreSQL 16-18
- Patch Cargo metadata to build with cargo-pgrx 0.18.1

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- Package upstream release v2.0.0 for PostgreSQL 16-18
- Normalize the pgrx-generated extension version to 2.0.0 during build
- Install the bundled Kazakh tsearch_data lexicon and stopword files
