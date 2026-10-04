%global pname pg_search
%global sname pg_search
%global srcdir paradedb-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global rust_toolchain stable
%global pgrx_version 0.19.3

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_search only supports PostgreSQL 15 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.26.0
Release:	1PGSTY%{?dist}
Summary:	Full text search over SQL tables using the BM25 algorithm
# Exact per-crate expressions are installed as third-party/LICENSE-EXPRESSIONS.txt.
# This aggregate enumerates every atomic license family in the resolved package closure.
License:	(AGPL-3.0-or-later) AND 0BSD AND Apache-2.0 AND (Apache-2.0 WITH LLVM-exception) AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND CC0-1.0 AND CDLA-Permissive-2.0 AND ISC AND MIT AND MPL-2.0 AND Unicode-3.0 AND Unlicense AND Zlib AND zlib-acknowledgement
URL:		https://github.com/paradedb/paradedb/
Source0:	pg_search-%{version}.tar.gz
Source1:	pg_search_collect_third_party_licenses.py
Patch0:		pg-search-0.26.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang git rust rustfmt openssl-devel openblas-devel pkgconfig python3
Requires:	postgresql%{pgmajorversion}-server pgvector_%{pgmajorversion}

%description
pg_search is a PostgreSQL extension that enables full text search over SQL tables using the BM25 algorithm,
the state-of-the-art ranking function for full text search.
It is built on top of Tantivy, the Rust-based alternative to Apache Lucene, using pgrx.
The module must be added to shared_preload_libraries and PostgreSQL restarted
before the extension can be created or used.

%prep
%setup -q -n %{srcdir}
patch --fuzz=0 --batch --forward -p1 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export RUSTUP_TOOLCHAIN=%{rust_toolchain}
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-%{_builddir}/%{srcdir}/target}"

CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "%{pgrx_version}" ]; then
	echo "cargo-pgrx %{pgrx_version} is required; run pig build pgrx -v %{pgrx_version} before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked

export CARGO_BUILD_JOBS="${CARGO_BUILD_JOBS:-2}"
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"

cd %{pname}
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
cd ..
TARGET_TRIPLE=$(rustc -vV | sed -n 's/^host: //p')
CARGO_NET_OFFLINE=true cargo metadata --locked --offline \
	--manifest-path %{pname}/Cargo.toml --no-default-features \
	--features pg%{pgmajorversion} --filter-platform "$TARGET_TRIPLE" \
	--format-version=1 > .cargo-metadata-pg-search.json
python3 %{SOURCE1} .cargo-metadata-pg-search.json third-party-licenses
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
TARGET_DIR="${CARGO_TARGET_DIR:-%{_builddir}/%{srcdir}/target}"
cp -a $TARGET_DIR/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a $TARGET_DIR/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a $TARGET_DIR/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/
install -d %{buildroot}%{_licensedir}/%{name}/third-party
cp -a third-party-licenses/. %{buildroot}%{_licensedir}/%{name}/third-party/

%files
%license LICENSE
%license %{_licensedir}/%{name}/third-party
%doc %{pname}/README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 0.26.0-1PGSTY
- Update to upstream 0.26.0.
- Build with pgrx and cargo-pgrx 0.19.3; retain a locked dependency graph.

* Thu Oct 01 2026 Vonng <rh@vonng.com> - 0.25.11-1PGSTY
- Update to upstream 0.25.11 with pgrx pinned to 0.19.2
- Preserve the locked dependency graph and complete debug packages

* Tue Sep 29 2026 Vonng <rh@vonng.com> - 0.25.10-1PGSTY
- Update to upstream 0.25.10 with pgrx pinned to 0.19.2
- Preserve the locked dependency graph and debug package payload

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.25.9-1PGSTY
- Update to 0.25.9

* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.25.6-1PGSTY
- Update to upstream PGXN 0.25.6
- Build the fixed Cargo graph with Rust 1.97.1 and cargo-pgrx 0.19.2
- Build from the locked Git dependency graph without mutating Cargo.lock
- Keep the upstream PostgreSQL 15 through 18 support matrix
- Align package metadata with upstream's AGPL-3.0-or-later source headers
- Ship license and notice files for the resolved static Rust dependency closure

* Wed Aug 12 2026 Vonng <rh@vonng.com> - 0.25.2-1PIGSTY
- Update to upstream PGXN 0.25.2
- Keep the validated cargo-pgrx 0.19.1 compatibility patch
- Document the new shared_preload_libraries requirement
- Package the upstream license and declare the Git build dependency

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 0.25.1-1PIGSTY
- Update to upstream PGXN 0.25.1
- Keep the validated cargo-pgrx 0.19.1 compatibility patch

* Thu Jul 30 2026 Vonng <rh@vonng.com> - 0.25.0-1PIGSTY
- Update to upstream PGXN 0.25.0
- Add the new OpenBLAS build dependency for SuperKMeans
- Add the new runtime dependency on pgvector
- Align upstream pgrx 0.19.0 dependencies with builder cargo-pgrx 0.19.1
- Use the validated builder stable Rust toolchain

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.24.3-1PIGSTY
- Update to upstream 0.24.3 and migrate all active pgrx workspace crates to 0.19.1
- Use the validated builder stable Rust toolchain without downloading another toolchain
- Drop the upstream rust-toolchain manifest so rustup does not refresh a moving channel during container builds

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.24.0-1PIGSTY
- Update to upstream PGXN 0.24.0 using the normalized source tarball
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Require preinstalled cargo-pgrx 0.18.1 and keep pgrx schema metadata during linking

* Fri Apr 17 2026 Vonng <rh@vonng.com> - 0.23.0-1PIGSTY
- Update to upstream 0.23.0 from the normalized PGXN source bundle

* Fri Apr 10 2026 Vonng <rh@vonng.com> - 0.22.6-1PIGSTY
- https://github.com/paradedb/paradedb/releases/tag/v0.22.6
- Repacked upstream tag with gtar into pg_search-0.22.6.tar.gz
* Mon Apr 06 2026 Vonng <rh@vonng.com> - 0.22.5-1PIGSTY
- https://github.com/paradedb/paradedb/releases/tag/v0.22.5
* Sat Mar 21 2026 Vonng <rh@vonng.com> - 0.22.2-1PIGSTY
* Thu Mar 05 2026 Vonng <rh@vonng.com> - 0.21.12-1PIGSTY
* Wed Feb 18 2026 Vonng <rh@vonng.com> - 0.21.8-1PIGSTY
- https://github.com/paradedb/paradedb/releases/tag/v0.21.8
* Sat Feb 07 2026 Vonng <rh@vonng.com> - 0.21.6-1PIGSTY
- https://github.com/paradedb/paradedb/releases/tag/v0.21.6
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 0.21.2-1PIGSTY
- bump to 0.21.2 with PG 15-18 support
* Wed Dec 24 2025 Vonng <rh@vonng.com> - 0.20.5-1PIGSTY
* Tue Dec 16 2025 Vonng <rh@vonng.com> - 0.20.4-1PIGSTY
* Mon Dec 15 2025 Vonng <rh@vonng.com> - 0.20.3-1PIGSTY
* Sat Nov 22 2025 Vonng <rh@vonng.com> - 0.20.0-1PIGSTY
* Tue Nov 18 2025 Vonng <rh@vonng.com> - 0.19.7-1PIGSTY
* Fri Jul 26 2024 Vonng <rh@vonng.com> - 0.8.6-1PIGSTY
* Mon Jul 22 2024 Vonng <rh@vonng.com> - 0.8.5-1PIGSTY
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.8.4-1PIGSTY
* Fri Jul 05 2024 Vonng <rh@vonng.com> - 0.8.2-1PIGSTY
* Sun Jun 30 2024 Vonng <rh@vonng.com> - 0.8.1-1PIGSTY
* Wed May 15 2024 Vonng <rh@vonng.com> - 0.7.0-1PIGSTY
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 0.6.1-1PIGSTY
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 0.5.6-1PIGSTY
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 0.5.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
