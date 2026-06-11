%define debug_package %{nil}
%global pname pgrdf
%global sname pgrdf
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 17
%{error:pgrdf only supports PostgreSQL 14 through 17}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.5.0
Release:	1PIGSTY%{?dist}
Summary:	RDF, SPARQL, SHACL, and OWL reasoning for PostgreSQL
License:	MIT
URL:		https://github.com/styk-tv/pgRDF
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgrdf/0.5.0/pgrdf-0.5.0.zip
#           Upstream pgrx 0.16 manifest declares PG14-PG17 features only.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pgrdf is a Rust-native PostgreSQL extension for RDF storage, SPARQL queries,
SHACL validation, and OWL reasoning.
For production deployments that use its shared-memory cache and hooks, load
pgrdf through shared_preload_libraries before starting PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.16.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch
cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{sname}-%{version}/README.pgxn.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{sname}-%{version}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.pgxn.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.5.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.5.0
- Document the shared_preload_libraries requirement for production hook setup
