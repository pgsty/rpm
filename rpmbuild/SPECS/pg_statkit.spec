%global pname pg_statkit
%global sname pg_statkit
%global pgrx_version 0.18.1
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 17
%{error:pg_statkit only supports PostgreSQL 14 through 17 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.1.0
Release:        1PGSTY%{?dist}
Summary:        Descriptive statistics and effect sizes for PostgreSQL
License:        MIT
URL:            https://github.com/kirdmi/pg_statkit
Source0:        pg_statkit-1.1.0.tar.gz
# Source: https://codeload.github.com/kirdmi/pg_statkit/tar.gz/v1.1.0
# SHA256: 2e438bd4e102f38649bec19988a54531bab520de9589e053907311df1ea66979

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo rust rustfmt clang
Requires:       postgresql%{pgmajorversion}-server

%description
Descriptive statistics and effect sizes for PostgreSQL.

%prep
%setup -q -n pg_statkit-1.1.0

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
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.1.0-1PGSTY
- Initial RPM package with pinned dependencies and native debug packages
