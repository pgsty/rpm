%define debug_package %{nil}
%global pname pg_cardano
%global sname pg_cardano
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_cardano only supports PostgreSQL 15 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.0
Release:	3PIGSTY%{?dist}
Summary:	Cardano-related tools, including cryptographic functions, address encoding/decoding, and blockchain data processing.
License:	MIT
URL:		https://github.com/cardano-community/pg_cardano
Source0:	pg_cardano-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
This extension is an attempt to create a Swiss Army knife for simplifying the work with binary data in Cardano db-sync, as well as automating some processes.
It is written in Rust, which ensures high security and excellent performance.
The extension is designed to handle unforeseen errors gracefully, without causing any disruptions in the database's operation. All errors are safely propagated as PostgreSQL-level error messages.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg-cardano-1.2.0.patch

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
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
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 1.2.0-3PIGSTY
- Migrate the direct-on-pristine source patch and locked dependency graph to pgrx 0.19.1
- Fetch the fixed Cargo.lock and verify cargo pgrx package does not rewrite it

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 1.2.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
- Package the pg_cardano-1.2.0.tar.gz source tree from cardano-community/pg_cardano
- Restrict packaging target to PostgreSQL 15 through 18 to match upstream features
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.1.1
* Wed May 07 2025 Vonng <rh@vonng.com> - 1.0.5
* Wed Dec 10 2024 Vonng <rh@vonng.com> - 1.0.3
* Sat Oct 19 2024 Vonng <rh@vonng.com> - 1.0.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
