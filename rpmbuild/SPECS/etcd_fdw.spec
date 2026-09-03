%global pname etcd_fdw
%global sname etcd_fdw
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:etcd_fdw supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	4PGSTY%{?dist}
Summary:	Foreign data wrapper for etcd
License:	MIT AND Apache-2.0
URL:		https://github.com/cybertec-postgresql/etcd_fdw
Source0:	etcd_fdw-%{version}.tar.gz
Source1:	wrappers-0.6.2.tar.gz
#           https://github.com/supabase/wrappers/archive/refs/tags/v0.6.2.tar.gz
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
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
mkdir -p %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{srcdir}/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE.etcd_fdw
install -m 644 %{_builddir}/%{srcdir}/vendor/wrappers/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE.wrappers

%files
%license %{_licensedir}/%{name}/LICENSE.etcd_fdw
%license %{_licensedir}/%{name}/LICENSE.wrappers
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.0.1-4PGSTY
- Vendor the formal Supabase Wrappers 0.6.2 source release
- Rebase the Cybertec cached-plan lifetime fix for Wrappers 0.6.2
- Build PostgreSQL 14 through 18 with pgrx and cargo-pgrx 0.19.2
- Install both the MIT and Apache-2.0 license texts

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
