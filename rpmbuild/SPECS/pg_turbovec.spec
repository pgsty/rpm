%global pname pg_turbovec
%global sname pg_turbovec
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_turbovec supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.14.1
Release:        1PGSTY%{?dist}
Summary:        TurboQuant-compressed vector search for PostgreSQL
License:        Apache-2.0
URL:            https://codeberg.org/gregburd/pg_turbovec
Source0:        %{sname}-%{version}.tar.gz
#               https://codeberg.org/gregburd/pg_turbovec/archive/v2.14.1.tar.gz
# Repacked with GNU tar to use a versioned archive root.
Patch0:         pg-turbovec-2.14.1.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang git rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
pg_turbovec provides compressed vector types and a PostgreSQL index access
method backed by the TurboQuant quantizer. It supports exact and approximate
nearest-neighbor search with L2, inner-product, cosine, and L1 distances.

%prep
%setup -q -n %{srcdir}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export RUSTUP_TOOLCHAIN=stable
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-%{_builddir}/%{srcdir}/target}"

PGRX_VERSION=0.19.3
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_HTTP_TIMEOUT=600 CARGO_NET_RETRY=10 CARGO_NET_GIT_FETCH_WITH_CLI=true \
    cargo fetch --locked

export CARGO_BUILD_JOBS="${CARGO_BUILD_JOBS:-2}"
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true \
    cargo pgrx package -v --no-default-features \
    --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
EXT_DIR="$CARGO_TARGET_DIR"/release/%{pname}-pg%{pgmajorversion}%{pginstdir}/share/extension
cp -f sql/%{pname}--*--*.sql "$EXT_DIR/"
test "$LOCK_SHA256" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
TARGET_DIR="${CARGO_TARGET_DIR:-%{_builddir}/%{srcdir}/target}"
PKGDIR="$TARGET_DIR/release/%{pname}-pg%{pgmajorversion}"
cp -a "$PKGDIR%{pginstdir}/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}"*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 docs/UPGRADING.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/UPGRADING.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Wed Oct 21 2026 Ruohang Feng <rh@vonng.com> - 2.14.1-1PGSTY
- Update to upstream 2.14.1.

* Thu Oct 15 2026 Ruohang Feng <rh@vonng.com> - 2.12.1-1PGSTY
- Update to upstream 2.12.1 and align the source patch with pgrx 0.19.3.

* Sat Oct 10 2026 Vonng <rh@vonng.com> - 2.12.0-1PGSTY
- Align pgrx and cargo-pgrx with the 0.19.3 Docker builder toolchain.
- Update to upstream 2.12.0 and align the locked pgrx graph with cargo-pgrx 0.19.3.
- Keep PostgreSQL 14 through 18 targets and the complete SQL upgrade chain.

* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 2.10.3-1PGSTY
- Update to 2.10.3.

* Sun Sep 06 2026 Vonng <rh@vonng.com> - 2.2.2-1PGSTY
- Update to official tag 2.2.2 with the locked pgrx 0.19.2 dependency graph
- Ship the SQL upgrade chain through 2.2.2 for PostgreSQL 14 through 18
- Retain wire v8; upgrades from 2.x do not require REINDEX

* Tue Sep 01 2026 Vonng <rh@vonng.com> - 2.0.0-1PGSTY
- Update to upstream pg_turbovec 2.0.0 and pgrx 0.19.2 for PostgreSQL 14-18
- Ship the complete 1.29.x upgrade chain and drop the obsolete OpenBLAS dependency
- Require restart, ALTER EXTENSION, and one REINDEX per turbovec index for wire v8

* Wed Aug 12 2026 Vonng <rh@vonng.com> - 1.29.0-1PIGSTY
- Update to upstream pg_turbovec 1.29.0

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 1.28.3-1PIGSTY
- Initial RPM release for pg_turbovec 1.28.3 and PostgreSQL 14 through 18
- Build with the upstream pgrx 0.19.1 dependency graph and OpenBLAS
