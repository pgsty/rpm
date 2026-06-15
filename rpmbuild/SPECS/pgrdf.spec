%define debug_package %{nil}
%global pname pgrdf
%global sname pgrdf
%global srcdir styk-tv-pgRDF-ff2f228
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 17
%{error:pgrdf only supports PostgreSQL 14 through 17}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.6.4
Release:	1PIGSTY%{?dist}
Summary:	RDF, SPARQL, SHACL, and OWL reasoning for PostgreSQL
License:	MIT
URL:		https://github.com/styk-tv/pgRDF
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgrdf/0.6.4/pgrdf-0.6.4.zip
#           Upstream manifest declares PG14-PG17 features only.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt git
Requires:	postgresql%{pgmajorversion}-server

%description
pgrdf is a Rust-native PostgreSQL extension for RDF storage, SPARQL queries,
SHACL validation, and OWL reasoning.
For production deployments that use its shared-memory cache and hooks, load
pgrdf through shared_preload_libraries before starting PostgreSQL.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{_specdir}/patches/pgrdf-0.6.4.patch

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
CARGO_NET_GIT_FETCH_WITH_CLI=true CARGO_HTTP_TIMEOUT=600 CARGO_NET_RETRY=10 cargo update -p pgrx --precise $PGRX_VERSION
CARGO_NET_GIT_FETCH_WITH_CLI=true CARGO_HTTP_TIMEOUT=600 CARGO_NET_RETRY=10 cargo update -p pgrx-tests --precise $PGRX_VERSION
CARGO_NET_GIT_FETCH_WITH_CLI=true CARGO_HTTP_TIMEOUT=600 CARGO_NET_RETRY=10 cargo fetch

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true CARGO_HTTP_TIMEOUT=600 CARGO_NET_RETRY=10 cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{srcdir}/README.pgxn.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.pgxn.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.6.4-1PIGSTY
- Package upstream release 0.6.4 for PostgreSQL 14-17
- Patch Cargo metadata to build with cargo-pgrx 0.18.1

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.5.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.5.0
- Document the shared_preload_libraries requirement for production hook setup
