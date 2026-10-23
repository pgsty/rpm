%global pname tin
%global sname lead
%global commit e3ed2f4ce1388167b0254a0c0c706a61d0a37d83
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:lead supports PostgreSQL 17 and 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.6
Release:        1PGSTY%{?dist}
Summary:        TIN-compatible text search for development and testing
License:        AGPL-3.0-or-later
URL:            https://github.com/planetscale/lead
Source0:        %{sname}-%{version}.tar.gz
# Untagged upstream snapshot; the official commit archive is kept unchanged.
# https://codeload.github.com/planetscale/lead/tar.gz/e3ed2f4ce1388167b0254a0c0c706a61d0a37d83

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang git rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
Lead implements the tin access method, TINQL matching, tokenization, scoring,
and highlighting for development, tests, and CI. It intentionally scans the
heap for exact matches and is unsuitable for production workloads. The SQL
extension is named tin and loads on demand without shared preload libraries.
This package contains an untagged upstream source snapshot.

%prep
%setup -q -n %{sname}-%{commit}

%build
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-%{_builddir}/%{sname}-%{commit}/target}"
PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
    echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
    exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
# Preserve upstream's Linux linker setting when adding the pgrx schema flags.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--unresolved-symbols=ignore-all -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true \
    cargo pgrx package -v --package %{pname} --no-default-features \
    --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_SHA256" = "$(sha256sum Cargo.lock | awk '{print $1}')"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
TARGET_DIR="${CARGO_TARGET_DIR:-%{_builddir}/%{sname}-%{commit}/target}"
PKGDIR="$TARGET_DIR/release/%{pname}-pg%{pgmajorversion}"
install -m 755 "$PKGDIR%{pginstdir}/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
install -m 644 "$PKGDIR%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
install -m 644 "$PKGDIR%{pginstdir}/share/extension/%{pname}"--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
# Rust/pgrx does not emit PGXS bitcode or an extension llvmjit package.

%changelog
* Fri Oct 23 2026 Ruohang Feng <rh@vonng.com> - 1.0.6-1PGSTY
- Package upstream snapshot e3ed2f4ce1388167b0254a0c0c706a61d0a37d83
  (2026-10-08) for PostgreSQL 17 and 18.
- Keep upstream Rust 1.96.0, pgrx 0.19.1, and locked dependencies.
- Preserve complete release debug information for debuginfo and debugsource.
