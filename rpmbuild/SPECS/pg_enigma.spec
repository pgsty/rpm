%define debug_package %{nil}
%global pname pg_enigma
%global sname pg_enigma
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_enigma only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.5.0
Release:	3PIGSTY%{?dist}
Summary:	Encrypted data type for PostgreSQL with PGP and RSA support
License:	MIT
URL:		https://github.com/SoftwareLibreMx/pg_enigma
Source0:	pg_enigma-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
BuildRequires:	openssl-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	openssl

%description
pg_enigma implements an encrypted data type allowing storage of encrypted data in
PostgreSQL columns. It provides PGP and RSA encryption with key management through
SQL functions, enabling transparent encryption and decryption of sensitive data
at the database level without application modifications.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg-enigma-0.5.0.patch

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
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.5.0-3PIGSTY
- Migrate the direct-on-pristine source patch and locked dependency graph to pgrx 0.19.1
- Preserve the custom SQL type translation compatibility changes and verify the lock remains fixed

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.5.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Mon Dec 15 2025 Vonng <rh@vonng.com> - 0.5.0-1PIGSTY
* Sun Nov 17 2025 Vonng <rh@vonng.com> - 0.4.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
