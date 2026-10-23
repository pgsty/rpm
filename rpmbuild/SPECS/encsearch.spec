%global pname encsearch
%global sname encsearch
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global pgrx_version 0.19.3

# Upstream currently validates PostgreSQL 17 only.
%if 0%{?pgmajorversion} != 17
%{error:encsearch currently supports PostgreSQL 17 only}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.1
Release:        1PGSTY%{?dist}
Summary:        Searchable encryption with keyed blind indexes for PostgreSQL
License:        BSD-3-Clause AND CC0-1.0 AND MIT AND PostgreSQL AND Unicode-3.0 AND Zlib
URL:            https://github.com/lokeshmulpuru/encsearch
Source0:        %{sname}-%{version}.tar.gz
Patch0:         encsearch-0.1.1-licenses.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rust rustfmt python3
Requires:       postgresql%{pgmajorversion}-server

%description
encsearch provides authenticated text encryption and keyed blind indexes for
exact, word, prefix and substring searches. It is an early upstream release.
Configure session_preload_libraries = 'encsearch' so the session key setting
is registered before clients set it. Blind indexes reveal matching tokens
and their frequencies; consult the upstream security notes before use.

%prep
%setup -q -n %{sname}-%{version}
%patch -P0 -p1

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
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
python3 packaging/collect-licenses.py cargo-license-metadata.json --pg pg%{pgmajorversion} --target "$BUILD_TARGET" --expected-license "BSD-3-Clause AND CC0-1.0 AND MIT AND PostgreSQL AND Unicode-3.0 AND Zlib"
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
PKGDIR=target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}
cp -a "$PKGDIR/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR/share/extension/"* %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE THIRD_PARTY_LICENSES
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 0.1.1-1PGSTY
- Initial RPM release for PostgreSQL 17
- Preserve upstream pgrx 0.19.3 dependencies and full release debug information
- Include reviewed licenses and copyrights for bundled Rust and native dependencies
