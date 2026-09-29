%global pname graph
%global sname pggraph
%global srcdir pggraph-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pggraph only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.1
Release:	1PGSTY%{?dist}
Summary:	Graph database capabilities for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/evokoa/pggraph
Source0:	%{sname}-%{version}.tar.gz
#           normalized from the official GitHub v1.2.1 tag archive
#           SQL extension payload is named graph.
Patch0:		pggraph-1.2.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pggraph packages the graph extension, which adds graph traversal and schema
registration capabilities to PostgreSQL. The PGXN distribution is named
pggraph, while the installed PostgreSQL extension is named graph.

%prep
%setup -q -n %{srcdir}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}/graph
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:/usr/bin:$PATH
export RUSTUP_TOOLCHAIN=stable

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo fetch --locked
# pgrx 0.19 embeds extension schema metadata in a linker section; without this
# flag the EL9A linker can garbage-collect it and cargo-pgrx reports a missing
# .pgrxsc section during packaging.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
EXT_DIR=target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}/share/extension
cp -f sql/%{pname}--*--*.sql "$EXT_DIR/"
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during package" >&2
	exit 1
}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{srcdir}/graph/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/graph/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/graph/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{srcdir}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/LICENSE %{buildroot}%{_licensedir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/NOTICE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/NOTICE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Tue Sep 29 2026 Vonng <rh@vonng.com> - 1.2.1-1PGSTY
- Update to upstream 1.2.1 with pgrx pinned to 0.19.2
- Preserve the locked dependency graph and debug package payload

* Wed Sep 02 2026 Vonng <rh@vonng.com> - 1.2.0-1PGSTY
- Update to upstream 1.2.0 and ship the 1.0 to 1.2 migration chain
- Build PostgreSQL 14 through 18 with pgrx and cargo-pgrx 0.19.2

* Mon Jul 27 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Update to upstream PGXN 1.0.0 with pgrx 0.19.1
- Keep Cargo.lock immutable and use the validated builder stable toolchain
- Preserve the upstream Apache NOTICE in the package payload

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.1.8-1PIGSTY
- Update to upstream v0.1.8 with native pgrx 0.19.1 support
- Use the validated builder stable Rust toolchain without downloading another toolchain

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 0.1.7-1PIGSTY
- Update to upstream PGXN 0.1.7
- Build with cargo-pgrx 0.18.1

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.1.5-1PIGSTY
- Initial RPM release for upstream PGXN 0.1.5
- Keep pgrx 0.18 schema metadata from being garbage-collected by the linker
