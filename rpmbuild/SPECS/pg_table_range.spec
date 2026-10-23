%global pname pg_table_range
%global sname pg_table_range
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global pgrx_version 0.18.1

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_table_range only supports PostgreSQL 16 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.2
Release:        1PGSTY%{?dist}
Summary:        Planning-time partition pruning by per-partition data ranges
License:        MIT AND Unicode-3.0 AND Zlib
URL:            https://github.com/bitner/pg_table_range
Source0:        %{sname}-%{version}.tar.gz
# Upstream omits Cargo.lock; freeze its pinned pgrx 0.18.1 dependency graph.
Patch0:         pg-table-range-0.1.2-lockfile.patch
Patch1:         pg-table-range-0.1.2-licenses.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rust rustfmt python3
Requires:       postgresql%{pgmajorversion}-server

%description
pg_table_range provides a custom table_range index access method and planner
hooks that prune partitions using summaries of their actual column values,
including non-partition-key columns. This is an experimental upstream release.
PostGIS is optional and adds geometry extent support. Large partition counts
may require a higher max_locks_per_transaction setting.

%prep
%setup -q -n %{sname}-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
# PGRX_BINDIR permits an isolated matching cargo-pgrx installation.
export PATH="${PGRX_BINDIR:-$HOME/.cargo/bin}":%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "%{pgrx_version}" ]; then
    echo "cargo-pgrx %{pgrx_version} is required; run pig build pgrx -v %{pgrx_version} before building" >&2
    exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
# Match the active feature and native target before collecting bundled licenses.
BUILD_TARGET=$(rustc -vV | sed -n 's/^host: //p')
cargo metadata --locked --offline --format-version=1 --no-default-features --features pg%{pgmajorversion} --filter-platform "$BUILD_TARGET" > cargo-license-metadata.json
python3 packaging/collect-licenses.py cargo-license-metadata.json --pg pg%{pgmajorversion} --target "$BUILD_TARGET" --expected-license "MIT AND Unicode-3.0 AND Zlib"
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
PKGDIR=target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}
cp -a "$PKGDIR/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR/share/extension/"* %{buildroot}%{pginstdir}/share/extension/
cp -a sql/%{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE THIRD_PARTY_LICENSES
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 0.1.2-1PGSTY
- Initial RPM release for PostgreSQL 16 through 18
- Preserve upstream pgrx 0.18.1, migration SQL and full release debug information
- Freeze the dependency graph omitted from the upstream source archive
- Include reviewed licenses and copyrights for bundled Rust and native dependencies
