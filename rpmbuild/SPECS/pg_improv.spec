%global pname pg_improv
%global sname pg_improv
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_improv only supports PostgreSQL 15 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.10.0
Release:        1PGSTY%{?dist}
Summary:        Incremental multidimensional models over PostgreSQL tables
License:        Apache-2.0 OR MIT
URL:            https://codeberg.org/gregburd/improv
Source0:        improv-%{version}.tar.gz
Patch0:         pg-improv-0.10.0-pgrx-0.19.3.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
pg_improv binds PostgreSQL tables to multidimensional models, evaluates
formulas and what-if scenarios, and maintains result tables incrementally.
Logical synchronization requires shared_preload_libraries = 'pg_improv'
and wal_level = logical. Manual and trigger modes also work without preload.
Numeric model values use double precision.

%prep
%setup -q -n improv-%{version}
%patch -P0 -p1

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
cd crates/pg_improv
PGRX_VERSION=0.19.3
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
    echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
    exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
PKGDIR=crates/pg_improv/target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}
cp -a "$PKGDIR/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR/share/extension/"* %{buildroot}%{pginstdir}/share/extension/
# Preserve upstream migration files; cargo-pgrx handles the generated base SQL.
cp -a crates/pg_improv/sql/%{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE-APACHE LICENSE-MIT
%doc crates/pg_improv/README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 0.10.0-1PGSTY
- Initial RPM release for PostgreSQL 15 through 18
- Build with pgrx 0.19.3 and the shared locked dependency patch
