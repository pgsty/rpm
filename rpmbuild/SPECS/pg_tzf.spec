%define debug_package %{nil}
%global pname tzf
%global sname pg_tzf
%global srcdir pg-tzf-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_tzf only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.1
Release:	1PGSTY%{?dist}
Summary:	Fast PG extension to lookup timezone name by GPS coordinates
License:	MIT AND ODbL-1.0
URL:		https://github.com/ringsaturn/pg-tzf
Source0:	pg-tzf-%{version}.tar.gz
#		https://github.com/ringsaturn/pg-tzf/archive/refs/tags/v0.3.1.tar.gz
#		v0.3.1 commit 31db8500308f8c01c7b4525da24ba68b9432c4b7
Patch0:		pg-tzf-0.3.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
Resolve IANA timezone names from longitude/latitude coordinates in PostgreSQL.

%prep
%setup -q -n %{srcdir}
patch -p1 --fuzz=0 < %{PATCH0}

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo fetch --locked

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
PKG_ROOT=target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}
EXT_DIR=$PKG_ROOT/share/extension
cp -f tzf--0.3.0--0.3.1.sql "$EXT_DIR/"
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
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
%doc README.md
%license LICENSE LICENSE_DATA
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.3.1-1PGSTY
- Update to upstream v0.3.1 (31db850) with pgrx 0.19.2 and tzf-rs 1.3.7
- Build PostgreSQL 14 through 18 with cargo-pgrx 0.19.2
- Add the catalog-preserving 0.3.0 to 0.3.1 extension update edge

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.3.0-2PIGSTY
- Build with cargo-pgrx 0.19.1 using the patched, locked dependency graph
- Use the validated image toolchain instead of downloading a floating nightly

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Bump to 0.3.0 and patch Cargo metadata to pgrx 0.18.1
- Use cargo-pgrx directly for version checks
- Use USTC rustup mirror for nightly toolchain setup

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2.4-1PIGSTY
- https://github.com/ringsaturn/pg-tzf/releases/tag/v0.2.4
- Drop the stale pgvector runtime dependency; upstream now uses PostgreSQL point types
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.2.3
* Thu May 22 2025 Vonng <rh@vonng.com> - 0.2.2
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.2.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
