%global pname typeid
%global sname pg_typeid
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_typeid only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.4.1
Release:	1PGSTY%{?dist}
Summary:	TypeID support for PostgreSQL
License:	MIT
URL:		https://github.com/blitss/typeid-postgres
Source0:	typeid-postgres-%{version}.tar.gz
Patch0:		pg-typeid-0.4.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
typeid-postgres enables native support for TypeIDs in PostgreSQL. TypeIDs are a modern
alternative to UUIDs based on UUIDv7, providing a human-readable prefix and a sortable
UUID suffix encoded in base32. This extension brings type-safe, sortable, and prefixed
unique identifiers to PostgreSQL, ideal for distributed systems and modern applications.

%prep
%setup -q -n typeid-postgres-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/typeid-postgres-%{version}
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
%ifarch x86_64
export RUSTFLAGS="${RUSTFLAGS:-} -C target-feature=+aes,+sse2"
%endif
%ifarch aarch64
export RUSTFLAGS="${RUSTFLAGS:-} -C target-feature=+aes,+neon"
%endif
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
EXT_DIR=target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}/share/extension
cp -f sql/%{pname}--*.sql "$EXT_DIR/"
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/typeid-postgres-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/typeid-postgres-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/typeid-postgres-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc Readme.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.4.1-1PGSTY
- Update to upstream 0.4.1 with the complete 0.3.0-to-0.4.1 SQL path
- Build PostgreSQL 14 through 18 with cargo-pgrx/pgrx 0.19.2
- Pin the dependency graph and retain architecture-specific gxhash AES flags

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.3.0-3PIGSTY
- Migrate the direct-on-pristine source patch and dependency graph to pgrx 0.19.1
- Add and enforce the upstream-absent Cargo.lock; enable gxhash AES/SSE2 on x86_64 and AES/NEON on aarch64

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.3.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging
- Enable gxhash AES/NEON target features on aarch64

* Mon Nov 17 2025 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
