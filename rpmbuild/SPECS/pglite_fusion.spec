%global pname pglite_fusion
%global sname pglite-fusion
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:pglite_fusion requires PostgreSQL 15 through 19}
%endif

Name:		%{pname}_%{pgmajorversion}
Version:	0.0.8
Release:	1PGSTY%{?dist}
Summary:	Embed an SQLite database in your PostgreSQL table. AKA multitenancy has been solved.
License:	MIT
URL:		https://github.com/frectonz/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/frectonz/pglite-fusion/archive/refs/tags/0.0.8.tar.gz
Patch0:		pglite-fusion-0.0.8-pgrx-0.20.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
Embed an SQLite database in your PostgreSQL table. AKA multitenancy has been solved.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export RUSTUP_TOOLCHAIN="${RUSTUP_TOOLCHAIN:-1.100.0}"
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.20.1
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
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Mon Nov 23 2026 Ruohang Feng <rh@vonng.com> - 0.0.8-1PGSTY
- Build with pgrx and cargo-pgrx 0.20.1 on Rust 1.100.0.

* Sun Nov 22 2026 Ruohang Feng <rh@vonng.com> - 0.0.8-1PGSTY
- Update to 0.0.8 and build for PostgreSQL 15 through 19 with pgrx 0.20.0.

* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.0.7-1PGSTY
- Update to upstream 0.0.7 and its rusqlite 0.40 runtime
- Build PostgreSQL 14 through 18 with pgrx and cargo-pgrx 0.19.2
- Add the catalog-neutral 0.0.6 to 0.0.7 extension update edge

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.0.6-4PIGSTY
- Migrate the direct-on-pristine source patch and dependency graph to pgrx 0.19.1
- Build offline after locked fetch and reject Cargo.lock rewrites

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.0.6-3PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Tue Nov 11 2025 Vonng <rh@vonng.com> - 0.0.6-1PIGSTY
- move from patched version to upstream official tag
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.0.5-2PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.0.5-1PIGSTY
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 0.0.4-1PIGSTY
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.0.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
