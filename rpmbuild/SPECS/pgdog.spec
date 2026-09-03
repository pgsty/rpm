%global sname pgdog
%global cfgdir %{_sysconfdir}/pgdog

Name:           %{sname}
Version:        0.1.56
Release:        1PGSTY%{?dist}
Summary:        Modern PostgreSQL proxy, pooler, load balancer and query router
License:        AGPL-3.0-only AND (MIT OR Apache-2.0) AND BSD-3-Clause AND PostgreSQL
URL:            https://github.com/pgdogdev/pgdog
Source0:        pgdog-%{version}.tar.gz
#               https://github.com/pgdogdev/pgdog/archive/refs/tags/v0.1.56.tar.gz
Source1:        pgdog-%{version}-vendor.tar.gz
Patch0:         pgdog-%{version}.patch

BuildRequires:  cargo, clang, clang-devel, cmake, gcc, gcc-c++, git, openssl-devel, pkgconf-pkg-config, protobuf-compiler, rust
BuildRequires:  systemd-rpm-macros
# Default pg_dump provider for schema-sync / resharding workflows and
# the default postgres service account expected by the systemd unit.
Requires:       ca-certificates, postgresql18-server, systemd

%description
PgDog is a PostgreSQL proxy, pooler, load balancer, sharder and query router
written in Rust. Version 0.1.56 uses the new parser and plugin ABI 0.4; custom
0.1.32 plugins must be rebuilt and manual query fingerprints retired.

%prep
%setup -q -n %{sname}-%{version}
mkdir -p vendor
tar -C vendor --strip-components=1 -xf %{SOURCE1}
mkdir -p packaging/rpm
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
export RUSTUP_TOOLCHAIN=1.96.1
export PGDOG_GIT_HASH=5d81522
export RUSTFLAGS="--cfg tokio_unstable"
if [ "%{_arch}" = "aarch64" ]; then
  export RUSTFLAGS="$RUSTFLAGS -C target-feature=+lse"
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
PATH=~/.cargo/bin:$PATH cargo fetch --locked
PATH=~/.cargo/bin:$PATH CARGO_NET_OFFLINE=true cargo build --release --locked -p pgdog
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')"
target/release/pgdog --version | grep -Fq 'PgDog v0.1.56 (5d81522)'
target/release/pgdog -c packaging/rpm/pgdog.toml -u packaging/rpm/users.toml configcheck

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{cfgdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_localstatedir}/lib/pgsql/pgdog

install -pm 0755 target/release/pgdog %{buildroot}%{_bindir}/pgdog
install -pm 0644 packaging/rpm/pgdog.service %{buildroot}%{_unitdir}/pgdog.service
install -pm 0644 packaging/rpm/pgdog.toml %{buildroot}%{cfgdir}/pgdog.toml
install -pm 0644 packaging/rpm/users.toml %{buildroot}%{cfgdir}/users.toml
install -d %{buildroot}%{_licensedir}/%{name}/third-party
install -pm 0644 vendor/pg_raw_parse/LICENSE-APACHE %{buildroot}%{_licensedir}/%{name}/third-party/pg_raw_parse-LICENSE-APACHE
install -pm 0644 vendor/pg_raw_parse/LICENSE-MIT %{buildroot}%{_licensedir}/%{name}/third-party/pg_raw_parse-LICENSE-MIT
install -pm 0644 vendor/pg_raw_parse/libpg_query/LICENSE %{buildroot}%{_licensedir}/%{name}/third-party/libpg_query-LICENSE
install -pm 0644 vendor/pg_raw_parse/libpg_query/src/postgres/COPYRIGHT %{buildroot}%{_licensedir}/%{name}/third-party/PostgreSQL-COPYRIGHT
install -pm 0644 vendor/scram/LICENSE %{buildroot}%{_licensedir}/%{name}/third-party/scram-LICENSE

%post
%systemd_post pgdog.service

%preun
%systemd_preun pgdog.service

%postun
%systemd_postun_with_restart pgdog.service

%files
%license LICENSE
%license %{_licensedir}/%{name}/third-party/*
%doc README.md
%doc example.pgdog.toml
%doc example.users.toml

%{_bindir}/pgdog
%{_unitdir}/pgdog.service

%dir %attr(0750,root,postgres) %{cfgdir}
%config(noreplace) %attr(0640,root,postgres) %{cfgdir}/pgdog.toml
%config(noreplace) %attr(0640,root,postgres) %{cfgdir}/users.toml

%dir %attr(0750,postgres,postgres) %{_localstatedir}/lib/pgsql/pgdog

%changelog
* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.1.56-1PGSTY
- Update to upstream PgDog 0.1.56 and preserve deterministic source identity
- Vendor pg_raw_parse, libpg_query, and scram for locked offline builds
- Account for the licenses of the statically linked parser and SCRAM sources
- Preserve tokio_unstable and ARM64 LSE without requiring mold
- Record the plugin ABI 0.4 and removed manual-query/fingerprint migration

* Sat Mar 21 2026 Vonng <rh@vonng.com> - 0.1.32-1PIGSTY
- Initial RPM release for PgDog with systemd service and default configuration
