%global pname pg_trickle
%global sname pg_trickle
%global srcdir pg-trickle-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_trickle only supports PostgreSQL 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.108.1
Release:	1PGSTY%{?dist}
Summary:	Streaming tables with differential view maintenance for PostgreSQL 18
License:	Apache-2.0
URL:		https://github.com/trickle-labs/pg-trickle
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg-trickle-0.108.1.patch
#           https://github.com/trickle-labs/pg-trickle/releases/tag/v0.108.1

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt openssl-devel pkgconfig
Requires:	postgresql%{pgmajorversion}-server

%description
pg_trickle turns PostgreSQL 18 into a real-time data platform with streaming
tables and incremental view maintenance, implemented as a pgrx extension.
Full background scheduler and shared-memory functionality require loading
pg_trickle through shared_preload_libraries.
The pg_trickle_dump definition-export tool is installed in the PostgreSQL 18
binary directory.

%prep
%setup -q -n %{srcdir}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export RUSTUP_TOOLCHAIN=1.98.0

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo build --release --locked --no-default-features --features pg%{pgmajorversion} --bin pg_trickle_dump
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/bin %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
mkdir -p %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 755 %{_builddir}/%{srcdir}/target/release/pg_trickle_dump %{buildroot}%{pginstdir}/bin/
install -m 644 %{_builddir}/%{srcdir}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/INSTALL.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/CHANGELOG.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/PACKAGING-UPGRADE.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/INSTALL.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%doc %{_docdir}/%{name}/PACKAGING-UPGRADE.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/bin/pg_trickle_dump
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 0.108.1-1PGSTY
- Update to 0.108.1.

* Tue Sep 29 2026 Vonng <rh@vonng.com> - 0.108.0-1PGSTY
- Update to upstream 0.108.0 with pgrx pinned to 0.19.2.
- Preserve the locked dependency graph, upgrade safeguards and pg_trickle_dump.

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.107.0-1PGSTY
- Update to 0.107.0

* Thu Sep 03 2026 Vonng <rh@vonng.com> - 0.92.0-1PGSTY
- Update to the signed upstream v0.92.0 tag archive
- Keep PostgreSQL 18 on cargo-pgrx and pgrx 0.19.2 with a locked dependency graph
- Ship all 29 update edges from 0.81.0 through 0.92.0 and the recovery safeguards
- Refresh the downstream migration guide for the 0.92.0 capture identity boundary

* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.90.0-1PGSTY
- Update to the signed upstream v0.90.0 tag archive
- Rebase to cargo-pgrx/pgrx 0.19.2 with locked dependencies
- Ship the upstream update scripts and pg_trickle_dump
- Repair upgrade descriptor/catalog parity and preserve default function metadata
- Document terminal consumer resnapshot and guarded V1 buffer cleanup

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.81.0-3PIGSTY
- Build with cargo-pgrx 0.19.1 and a locked dependency graph
- Preserve the packaging-only target trim and missing-generator guard

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.81.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.81.0-1PIGSTY
- Update to upstream PGXN 0.81.0 with the normalized source tarball
- Refresh the packaging-only Cargo/build.rs patch for the current PGXN bundle
- Keep pgrx 0.18 schema metadata from being garbage-collected by the linker

* Sun May 24 2026 Vonng <rh@vonng.com> - 0.71.0-1PIGSTY
- Update to upstream PGXN 0.71.0 with the normalized source tarball
- Refresh the packaging-only Cargo/build.rs patch for the current PGXN bundle

* Thu Apr 30 2026 Vonng <rh@vonng.com> - 0.40.0-1PIGSTY
- Update to upstream PGXN 0.40.0 with the normalized source tarball
- Refresh the packaging-only Cargo patch for pgrx 0.18.0 and the current workspace layout

* Sat Apr 25 2026 Vonng <rh@vonng.com> - 0.31.0-1PIGSTY
- Update to upstream PGXN 0.31.0 with the normalized source tarball
- Refresh the packaging-only Cargo patch for pgrx 0.18.0 and the expanded workspace
- Keep pgrx 0.18 schema metadata from being garbage-collected by the linker

* Fri Apr 17 2026 Vonng <rh@vonng.com> - 0.20.0-1PIGSTY
- Update to upstream 0.20.0 with the normalized PGXN source bundle
- Refresh the packaging-only Cargo target trim patch for the expanded bench set
- Keep patching cached pgrx 0.17.0 to avoid the Rust toolchain
  NonNull::from_mut incompatibility on the current EL builders

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.17.0-1PIGSTY
- Update to upstream 0.17.0 with the normalized pg_trickle-0.17.0.tar.gz source tarball
- Keep trimming the non-extension workspace/test targets for EL9A package builds
- Keep patching cached pgrx 0.17.0 to avoid the Rust toolchain
  NonNull::from_mut incompatibility on the current EL9A builders

* Wed Apr 08 2026 Vonng <rh@vonng.com> - 0.16.0-1PIGSTY
- https://github.com/grove/pg-trickle/releases/tag/v0.16.0

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.15.0-1PIGSTY
- Initial RPM release, PG18-only
