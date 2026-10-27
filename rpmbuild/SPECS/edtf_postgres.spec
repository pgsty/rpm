%global pname edtf_postgres
%global sname edtf_postgres
%global pgrx_version 0.19.3
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:edtf_postgres only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.3.2
Release:        1PGSTY%{?dist}
Summary:        Extended Date Time Format functions for PostgreSQL
License:        MIT OR Apache-2.0
URL:            https://github.com/monumental-archive/edtf
Source0:        edtf_postgres-1.3.2.tar.gz
Patch0:         edtf-postgres-1.3.2-pgrx-0.19.3.patch
# Source: https://codeload.github.com/monumental-archive/edtf/tar.gz/refs/tags/v1.3.2
# Commit: ef6872859274e67867c623771694960cdeef60a1
# Repacked with the historical edtf-edtf-postgres-v1.3.2 root and normalized
# permissions; source contents and executable bits match the upstream tag.
# SHA256: 139ffd3675a8cbcca780f9c511dcf8b8f3f2e8a3aa46f6c9aade35e7b8ac0cc2

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo rust rustfmt clang
Requires:       postgresql%{pgmajorversion}-server

%description
Extended Date Time Format functions for PostgreSQL.

%prep
%setup -q -n edtf-edtf-postgres-v1.3.2
%patch -P0 -p1

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
cd crates/edtf-postgres
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config --out-dir %{_builddir}/%{sname}-package
cd ../..
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
test "$LOCK_BEFORE" = "$LOCK_AFTER"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}
cp -a %{_builddir}/%{sname}-package%{pginstdir}/. %{buildroot}%{pginstdir}/

%files
%license LICENSE-APACHE LICENSE-MIT
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Tue Oct 27 2026 Vonng <rh@vonng.com> - 1.3.2-1PGSTY
- Update edtf_postgres to 1.3.2 and build with pgrx 0.19.3.
- Install the Apache and MIT license files shipped in the release.

* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.2.3-1PGSTY
- Initial RPM package with pinned dependencies and native debug packages
