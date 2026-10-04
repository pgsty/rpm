%global pname pg_money
%global sname pg_money
%global pgrx_version 0.19.2
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_money only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.3.0
Release:        1PGSTY%{?dist}
Summary:        Precise currency-aware money types for PostgreSQL
License:        MIT
URL:            https://github.com/RustedBytes/pg-money
Source0:        pg_money-0.3.0.tar.gz
# Source: https://codeload.github.com/RustedBytes/pg-money/tar.gz/v0.3.0
# SHA256: 2b9c12ab9c17115685983548d211fa618143a70a1e01d08f91636848b5bf469b

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo rust rustfmt clang
Requires:       postgresql%{pgmajorversion}-server

%description
Precise currency-aware money types for PostgreSQL.

%prep
%setup -q -n pg-money-0.3.0

%build
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
export CARGO_BUILD_JOBS=4
export PATH=/opt/pgrx-%{pgrx_version}/bin:%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
CURRENT_PGRX=$(cargo pgrx --version | awk '{print $2}')
test "$CURRENT_PGRX" = "%{pgrx_version}"
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config --out-dir %{_builddir}/%{sname}-package
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
test "$LOCK_BEFORE" = "$LOCK_AFTER"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}
cp -a %{_builddir}/%{sname}-package%{pginstdir}/. %{buildroot}%{pginstdir}/

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 0.3.0-1PGSTY
- Initial RPM package with pinned dependencies and native debug packages
