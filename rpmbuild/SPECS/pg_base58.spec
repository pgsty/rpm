%define debug_package %{nil}
%global pname pg_base58
%global sname pg_base58
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_base58 only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	2PGSTY%{?dist}
Summary:	Base58 Encoder/Decoder Extension for PostgreSQL
License:	MIT
URL:		https://github.com/Vonng/pg_base58
Source0:	pg_base58-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang rust-toolchain >= 1.96.0 cargo-pgrx-0191
Requires:	postgresql%{pgmajorversion}-server

%description
Base58 Encoder/Decoder Extension for PostgreSQL

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg-base58-0.0.1.patch

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$PATH
export PGRX_HOME=%{_builddir}/.pgrx-0191-pg%{pgmajorversion}
unset RUSTUP_HOME RUSTUP_TOOLCHAIN

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo-pgrx-0191 --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx-0191 $PGRX_VERSION is required" >&2
	exit 1
fi
RUST_VERSION=$(rust-toolchain rustc --version | awk '{print $2}')
if [ "$(printf '%s\n' 1.96.0 "$RUST_VERSION" | sort -V | head -1)" != "1.96.0" ]; then
	echo "rust-toolchain 1.96 or newer is required, found $RUST_VERSION" >&2
	exit 1
fi
cargo-pgrx-0191 init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true rust-toolchain cargo fetch --locked
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo-pgrx-0191 package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
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
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Thu Aug 20 2026 Vonng <rh@vonng.com> - 0.0.1-2PGSTY
- Build with packaged rust-toolchain and cargo-pgrx-0191
- Isolate PGRX_HOME from rustup and other cargo-pgrx slots

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.0.1-4PIGSTY
- Migrate the direct-on-pristine source patch and locked dependency graph to pgrx 0.19.1
- Fetch the fixed Cargo.lock and verify cargo pgrx package does not rewrite it

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.0.1-3PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.0.1-2PIGSTY
* Sat Oct 19 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
