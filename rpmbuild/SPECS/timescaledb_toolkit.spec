%global pname timescaledb_toolkit
%global sname timescaledb-toolkit
%global srcdir timescaledb-toolkit-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}
%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:timescaledb_toolkit 1.26 supports PostgreSQL 16 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.26.0
Release:	1PGSTY%{?dist}
Summary:	Analytical hyperfunctions for PostgreSQL and TimescaleDB
License:	LicenseRef-Timescale
URL:		https://github.com/timescale/timescaledb-toolkit
Source0:	%{sname}-%{version}.tar.gz
#           https://codeload.github.com/timescale/timescaledb-toolkit/tar.gz/refs/tags/1.26.0
Patch0:		timescaledb-toolkit-1.26.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt gcc make pkgconfig openssl-devel
Requires:	postgresql%{pgmajorversion}-server

%description
TimescaleDB Toolkit provides approximate aggregates, counter and gauge
analysis, time-weighted averages, state tracking, downsampling, and SQL
pipeline utilities for PostgreSQL and TimescaleDB. This package supports
PostgreSQL 16 through 18.

%prep
%setup -q -n %{srcdir}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export RUSTUP_TOOLCHAIN=stable
export CARGO_INCREMENTAL=0

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
(cd extension && cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run)
cargo fetch --locked

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
(cd extension && CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config)
PKGROOT=target/release/%{pname}-pg%{pgmajorversion}
CARGO_NET_OFFLINE=true cargo run --locked --manifest-path tools/post-install/Cargo.toml -- --dir "$PKGROOT"
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
mkdir -p %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
PKGROOT=%{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}
cp -a "$PKGROOT%{pginstdir}/lib/%{pname}-%{version}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGROOT%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGROOT%{pginstdir}/share/extension/%{pname}"--*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 README.md CHANGELOG.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE NOTICE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/NOTICE
%{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id

%changelog
* Wed Sep 02 2026 Vonng <rh@vonng.com> - 1.26.0-1PGSTY
- Update to upstream 1.26.0 for PostgreSQL 16 through 18
- Build with pgrx and cargo-pgrx 0.19.2 using the locked dependency graph
- Run the upstream post-install generator and ship all 21 direct upgrade paths
- Install the versioned shared library together with README, LICENSE, and NOTICE

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 1.23.0-2PIGSTY
- Build with cargo-pgrx 0.19.1 and a locked dependency graph
- Keep release debuginfo disabled and preserve linker metadata retention
- Synchronize the upstream pgrx version helper and install documentation

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 1.23.0-1PIGSTY
- https://github.com/timescale/timescaledb-toolkit/releases/tag/1.23.0
- Patch Cargo metadata to build with cargo-pgrx 0.18.1
- Disable release debuginfo to keep EL builder memory bounded

* Mon Oct 27 2025 Vonng <rh@vonng.com> - 1.22.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 1.21.0-1PIGSTY
* Thu Jan 23 2025 Vonng <rh@vonng.com> - 1.19.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
