%global pname stannum
%global sname stannum
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global source_commit 7573fc49a48486b7acc9a1107545b515ef9a83f3

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:stannum only supports PostgreSQL 17 and 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        Experimental TINQL text search and BM25 ranking for PostgreSQL
License:        AGPL-3.0-or-later
URL:            https://github.com/TeamSpringbird/stannum
Source0:        stannum-%{version}.tar.gz
# Pristine upstream commit archive; the SQL extension version remains 0.1.0.

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang git rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
Stannum is an experimental PostgreSQL text-search extension with TINQL,
BM25 ranking and persistent segmented indexes. This is an unreleased source
snapshot. Do not install stannum and tin in the same database: their global
operators conflict. Preloading is optional for primary-server queries and
required on primary and standby for standby index reads.

%prep
%setup -q -n %{sname}-%{source_commit}

%build
export PATH=$HOME/.cargo/bin:%{pginstdir}/bin:$PATH
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
# rust-toolchain.toml selects upstream Rust 1.96.0.
test "$(cargo pgrx --version | awk '{print $2}')" = 0.19.1
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
sha256sum Cargo.lock > .cargo-lock.before
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
# Keep upstream Linux link flags while retaining symbols needed by pgrx schema.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--unresolved-symbols=ignore-all -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package --package stannum --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config --out-dir pgstaging
sha256sum -c .cargo-lock.before

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
install -m 755 pgstaging%{pginstdir}/lib/stannum.so %{buildroot}%{pginstdir}/lib/
install -m 644 pgstaging%{pginstdir}/share/extension/stannum.control %{buildroot}%{pginstdir}/share/extension/
install -m 644 pgstaging%{pginstdir}/share/extension/stannum*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/stannum.so
%{pginstdir}/share/extension/stannum.control
%{pginstdir}/share/extension/stannum*.sql
%exclude /usr/lib/.build-id
# cargo-pgrx produces native Rust ELF; there is no PGXS bitcode payload.

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Package the unreleased upstream snapshot 7573fc49a48486b7acc9a1107545b515ef9a83f3 (2026-10-19)
- Build PostgreSQL 17 and 18 with upstream Rust 1.96.0 and pgrx 0.19.1
- Preserve the locked dependency graph and native debug packages
