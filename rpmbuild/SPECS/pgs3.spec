%global pname pgs3
%global sname pgs3
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pgs3 supports PostgreSQL 17 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.1
Release:        1PGSTY%{?dist}
Summary:        S3-compatible object storage inside PostgreSQL
License:        Apache-2.0
URL:            https://github.com/pgsty/pgs3
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/pgsty/pgs3/releases/tag/v0.1.1

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rustfmt
BuildRequires:  rust >= 1.85
Requires:       postgresql%{pgmajorversion}-server

%description
pgs3 provides a path-style S3-compatible HTTP endpoint from PostgreSQL
background workers, with SigV4 authentication and SQL-backed object storage.
Full endpoint functionality requires pgs3 in shared_preload_libraries.

%prep
%setup -q -n %{srcdir}
grep -Eq '^version[[:space:]]*=[[:space:]]*"%{version}"[[:space:]]*$' Cargo.toml

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
PKGROOT=%{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}
cp -a "$PKGROOT%{pginstdir}/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGROOT%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGROOT%{pginstdir}/share/extension/%{pname}"--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md docs/guc.md docs/known-limitations.md docs/operations.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Sep 03 2026 Vonng <rh@vonng.com> - 0.1.1-1PGSTY
- Initial RPM release for PostgreSQL 17 through 18
- Package the canonical upstream v0.1.1 source release
- Build with cargo-pgrx and pgrx 0.19.2 using the locked dependency graph
