%define debug_package %{nil}
%global pname etcd_fdw
%global sname etcd_fdw
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	3PIGSTY%{?dist}
Summary:	Foreign data wrapper for etcd
License:	MIT
URL:		https://github.com/cybertec-postgresql/etcd_fdw
Source0:	etcd_fdw-%{version}.tar.gz
Source1:	wrappers-0.6.1.tar.gz
Patch0:		etcd-fdw-0.0.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
BuildRequires:	protobuf-compiler
Requires:	postgresql%{pgmajorversion}-server

%description
etcd_fdw is a PostgreSQL foreign data wrapper for etcd,
the distributed key-value store used for shared configuration and service discovery.

%prep
%setup -q -n %{srcdir}
mkdir -p vendor/wrappers
tar -C vendor/wrappers --strip-components=1 -xf %{SOURCE1}
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
ROOT_LOCK_EXPECTED=39c99a4da5091d4a5d9700c6459b6b95f0c08ea8d0903679601d4014afaeffcf
VENDOR_LOCK_EXPECTED=8fb19f9bce4a2766ea8a2c64846e2b081e9f981f4bb10dd4eb615744b0493191
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
VENDOR_LOCK_BEFORE=$(sha256sum vendor/wrappers/Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$ROOT_LOCK_EXPECTED" ]; then
	echo "unexpected root Cargo.lock checksum: $LOCK_BEFORE" >&2
	exit 1
fi
if [ "$VENDOR_LOCK_BEFORE" != "$VENDOR_LOCK_EXPECTED" ]; then
	echo "unexpected vendor/wrappers Cargo.lock checksum: $VENDOR_LOCK_BEFORE" >&2
	exit 1
fi
OLD_PGRX=$(find . -name Cargo.toml -not -path './target/*' -exec grep -HE 'pgrx(-tests)?[[:space:]]*=.*0\.(12|16|17|18)' {} + || true)
if [ -n "$OLD_PGRX" ]; then
	echo "old pgrx dependency remains in a Cargo.toml:" >&2
	echo "$OLD_PGRX" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
VENDOR_LOCK_AFTER=$(sha256sum vendor/wrappers/Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ] || [ "$VENDOR_LOCK_BEFORE" != "$VENDOR_LOCK_AFTER" ]; then
	echo "a Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

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
%exclude /usr/lib/.build-id

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.0.1-3PIGSTY
- Migrate every vendored wrappers Cargo.toml and Cargo.lock to pgrx 0.19.1
- Gate both root and vendored lockfiles and reject recursive old pgrx declarations

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.0.1-2PIGSTY
- Build with cargo-pgrx 0.19.1 and a locked dependency graph
- Keep the vendored supabase-wrappers compatibility fixes in the source patch

* Sun Jun 14 2026 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Upgrade to upstream 0.0.1
- Vendor wrappers 0.6.1 and patch Cargo metadata for cargo-pgrx 0.18.1

* Sat Jan 17 2026 Vonng <rh@vonng.com> - 0.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
