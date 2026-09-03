%global pname pgcontext
%global sname pgcontext
%global srcdir pgContext-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pgcontext only supports PostgreSQL 17 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.0
Release:	1PGSTY%{?dist}
Summary:	Hybrid vector and full-text retrieval engine for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/Evokoa/pgContext
Source0:	%{sname}-%{version}.tar.gz
#           https://codeload.github.com/Evokoa/pgContext/tar.gz/refs/tags/v0.3.0
Patch0:		pgcontext-0.3.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server
Recommends:	pgvector_%{pgmajorversion}

%description
pgcontext provides dense vector search, metadata-filtered approximate search,
and hybrid dense plus full-text retrieval inside PostgreSQL. Version 0.3 is a
clean-install-only release for PostgreSQL 17 and 18. The retired
pgcontext_pgvector companion is replaced by an optional binding API in the
main extension.

%prep
%setup -q -n %{srcdir}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export RUSTUP_TOOLCHAIN=stable

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v -p context-pg --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during package" >&2
	exit 1
}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
PKGDIR=%{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}
cp -a "$PKGDIR%{pginstdir}/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}"*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 docs/user_guide/release_notes.md %{buildroot}%{_docdir}/%{name}/
install -m 644 docs/user_guide/pgvector_migration.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/
install -m 644 NOTICE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/release_notes.md
%doc %{_docdir}/%{name}/pgvector_migration.md
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/NOTICE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--0.3.0.sql
%exclude /usr/lib/.build-id/*

%changelog
* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.3.0-1PGSTY
- Update to the upstream 0.3.0 clean-install release for PostgreSQL 17 and 18
- Build with pgrx and cargo-pgrx 0.19.2 using the locked dependency graph
- Retire pgcontext_pgvector and require export/drop/create/rebuild from 0.2

* Mon Jul 27 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Add RPM package for PostgreSQL 17 and 18
- Build the upstream locked workspace with cargo-pgrx 0.19.1
- Preserve the upstream Apache NOTICE in the package payload
