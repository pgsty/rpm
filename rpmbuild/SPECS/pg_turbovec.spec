%define debug_package %{nil}
%global pname pg_turbovec
%global sname pg_turbovec
# Codeberg tag archives use the unversioned pg_turbovec/ root directory.
%global srcdir pg_turbovec
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_turbovec supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.29.0
Release:        1PGSTY%{?dist}
Summary:        TurboQuant-compressed vector search for PostgreSQL
License:        Apache-2.0
URL:            https://codeberg.org/gregburd/pg_turbovec
Source0:        %{sname}-%{version}.tar.gz
#               https://codeberg.org/gregburd/pg_turbovec/archive/v1.29.0.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang git rust rustfmt openblas-devel
Requires:       postgresql%{pgmajorversion}-server

%description
pg_turbovec provides compressed vector types and a PostgreSQL index access
method backed by the TurboQuant quantizer. It supports exact and approximate
nearest-neighbor search with L2, inner-product, cosine, and L1 distances.

%prep
%autosetup -n %{srcdir}

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
RUSTC_VERSION=$(rustc --version 2>/dev/null | awk '{print $2}')
echo "$RUSTC_VERSION" | awk 'NF {split($1, v, "."); if (v[1] > 1 || (v[1] == 1 && v[2] >= 96)) exit 0} {exit 1}' || {
	echo "rustc 1.96.0 or newer is required" >&2
	exit 1
}
grep -Fq 'rust-version = "1.96.0"' Cargo.toml
grep -Fq 'pgrx = "=0.19.1"' Cargo.toml
grep -Fq 'pgrx-tests = "=0.19.1"' Cargo.toml
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_HTTP_TIMEOUT=600 CARGO_NET_RETRY=10 CARGO_NET_GIT_FETCH_WITH_CLI=true \
    cargo fetch --locked

export CARGO_BUILD_JOBS="${CARGO_BUILD_JOBS:-2}"
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true \
    cargo pgrx package -v --no-default-features \
    --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_SHA256" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
PKGDIR=%{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}
test -d "$PKGDIR%{pginstdir}"
cp -a "$PKGDIR%{pginstdir}/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}"*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Wed Aug 12 2026 Vonng <rh@vonng.com> - 1.29.0-1PIGSTY
- Update to upstream pg_turbovec 1.29.0

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 1.28.3-1PIGSTY
- Initial RPM release for pg_turbovec 1.28.3 and PostgreSQL 14 through 18
- Build with the upstream pgrx 0.19.1 dependency graph and OpenBLAS
