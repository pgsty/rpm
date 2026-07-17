%define debug_package %{nil}
%global pname pg_search
%global sname pg_search
%global srcdir paradedb-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_search only supports PostgreSQL 15 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.24.3
Release:	1PIGSTY%{?dist}
Summary:	Full text search over SQL tables using the BM25 algorithm
License:	AGPL-3.0
URL:		https://github.com/paradedb/paradedb/
Source0:	pg_search-%{version}.tar.gz
#           https://github.com/paradedb/paradedb/archive/refs/tags/v0.24.3.tar.gz
Patch0:		pg-search-0.24.3.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt openssl-devel pkgconfig
Requires:	postgresql%{pgmajorversion}-server

%description
pg_search is a PostgreSQL extension that enables full text search over SQL tables using the BM25 algorithm,
the state-of-the-art ranking function for full text search.
It is built on top of Tantivy, the Rust-based alternative to Apache Lucene, using pgrx.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export RUSTUP_TOOLCHAIN=stable

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')

export CARGO_BUILD_JOBS="${CARGO_BUILD_JOBS:-2}"
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"

cd %{pname}
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_SHA256" = "$(sha256sum ../Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during package" >&2
	exit 1
}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.24.3-1PIGSTY
- Update to upstream 0.24.3 and migrate all active pgrx workspace crates to 0.19.1
- Use the validated builder stable Rust toolchain without downloading another toolchain

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
