%global pname pg_lexo
%global sname pg_lexo
%global pgrx_version 0.16.1
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_lexo only supports PostgreSQL 16 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.6.1
Release:        1PGSTY%{?dist}
Summary:        Lexicographic position keys for PostgreSQL
License:        MIT
URL:            https://github.com/Blad3Mak3r/pg_lexo
Source0:        pg_lexo-0.6.1.tar.gz
# Source: https://codeload.github.com/Blad3Mak3r/pg_lexo/tar.gz/v0.6.1
# SHA256: a9a7e21538f20199d4cdfb7168c8eb51761464bac38c5b73aa77c8e4c57f65a3
Source1:        pg_lexo-0.6.1-Cargo.lock
# Upstream release v0.6.1 retains Cargo/extension version 0.6.0.

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo rust rustfmt clang
Requires:       postgresql%{pgmajorversion}-server

%description
Lexicographic position keys for PostgreSQL.

%prep
%setup -q -n pg_lexo-0.6.1
cp %{SOURCE1} Cargo.lock

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
# pgrx 0.16 builds a schema helper that needs normal linker section GC.
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config --out-dir %{_builddir}/%{sname}-package
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
test "$LOCK_BEFORE" = "$LOCK_AFTER"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}
cp -a %{_builddir}/%{sname}-package%{pginstdir}/. %{buildroot}%{pginstdir}/

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 0.6.1-1PGSTY
- Initial RPM package with pinned dependencies and native debug packages
