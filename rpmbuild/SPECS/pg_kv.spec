%global pname pg_kv
%global sname pg_kv
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_kv only supports PostgreSQL 15 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        Shared-memory key/value cache, rate limits and sorted sets
License:        PostgreSQL
URL:            https://github.com/Murat7Ay/pg_kv
Source0:        %{sname}-%{version}.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
pg_kv provides a shared-memory key/value cache with TTL, token-bucket rate
limits and sorted sets. It requires shared_preload_libraries and uses one
nontransactional, nonpersistent keyspace across all databases in the cluster.
This is an early upstream release, not intended for production use.

%prep
%setup -q -n %{sname}-%{version}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

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
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
    echo "Cargo.lock changed during cargo pgrx package" >&2
    exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Initial RPM release with pgrx 0.19.3 and locked upstream dependencies
- Preserve release debug information for debuginfo and debugsource packages
