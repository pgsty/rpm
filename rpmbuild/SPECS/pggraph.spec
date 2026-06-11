%define debug_package %{nil}
%global pname graph
%global sname pggraph
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pggraph only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.7
Release:	1PIGSTY%{?dist}
Summary:	Graph database capabilities for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/evokoa/pggraph
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pggraph/0.1.7/pggraph-0.1.7.zip
#           SQL extension payload is named graph.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pggraph packages the graph extension, which adds graph traversal and schema
registration capabilities to PostgreSQL. The PGXN distribution is named
pggraph, while the installed PostgreSQL extension is named graph.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}/graph
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:/usr/bin:$PATH

PGRX_VERSION=0.18.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch
# pgrx 0.18 embeds extension schema metadata in a linker section; without this
# flag the EL9A linker can garbage-collect it and cargo-pgrx reports a missing
# .pgrxsc section during packaging.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{sname}-%{version}/graph/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/graph/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/graph/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{sname}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{sname}-%{version}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 11 2026 Vonng <rh@vonng.com> - 0.1.7-1PIGSTY
- Update to upstream PGXN 0.1.7
- Build with cargo-pgrx 0.18.1

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.1.5-1PIGSTY
- Initial RPM release for upstream PGXN 0.1.5
- Keep pgrx 0.18 schema metadata from being garbage-collected by the linker
