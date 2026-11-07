%global sname pg_warren
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_warren supports PostgreSQL 15 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.8.0
Release:        1PGSTY%{?dist}
Summary:        Graph traversal and computation over PostgreSQL tables
License:        Apache-2.0
URL:            https://github.com/ExaDev/pg_warren
Source0:        %{sname}-%{version}.tar.gz
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
pg_warren builds versioned adjacency snapshots from relational tables and
provides graph traversal, PageRank, community detection and graph computation
through SQL. PostgreSQL 15-16 require preload for the optional shared cache.

%prep
%setup -q -n %{sname}-%{version}

%build
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
# Builder stable Rust satisfies upstream's Rust 1.97 minimum.
export RUSTUP_TOOLCHAIN="${RUSTUP_TOOLCHAIN:-stable}"
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
test "$(cargo pgrx --version | awk '{print $2}')" = 0.19.3
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
sha256sum Cargo.lock > .cargo-lock.before
cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v \
    --manifest-path crates/pg_warren/Cargo.toml \
    --no-default-features --features pg%{pgmajorversion} \
    --pg-config %{pginstdir}/bin/pg_config --out-dir "$PWD/package"
sha256sum -c .cargo-lock.before

%install
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
install -m 755 package%{pginstdir}/lib/pg_warren.so %{buildroot}%{pginstdir}/lib/
install -m 644 package%{pginstdir}/share/extension/pg_warren.control %{buildroot}%{pginstdir}/share/extension/
install -m 644 package%{pginstdir}/share/extension/pg_warren--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE NOTICE
%doc README.md docs/limits.md
%{pginstdir}/lib/pg_warren.so
%{pginstdir}/share/extension/pg_warren.control
%{pginstdir}/share/extension/pg_warren--*.sql

%changelog
* Fri Nov 06 2026 Ruohang Feng <rh@vonng.com> - 0.8.0-1PGSTY
- Package upstream 0.8.0 with pgrx 0.19.3 for PostgreSQL 15-18.
- Preserve release DWARF and the upstream SQL upgrade scripts.
