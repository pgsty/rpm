%define debug_package %{nil}
%global sname pgdog
%global cfgdir %{_sysconfdir}/pgdog

Name:           %{sname}
Version:        0.1.32
Release:        1PIGSTY%{?dist}
Summary:        Modern PostgreSQL proxy, pooler, load balancer and query router
License:        AGPL-3.0
URL:            https://github.com/pgdogdev/pgdog
Source0:        pgdog-%{version}.tar.gz
#               https://github.com/pgdogdev/pgdog/archive/refs/tags/v0.1.32.tar.gz

# cargo/rust are provisioned manually on builders via `pig build rust`,
# so they are intentionally not declared as BuildRequires here.
BuildRequires:  clang, cmake, gcc, gcc-c++, git, openssl-devel, pkgconf-pkg-config, protobuf-compiler
BuildRequires:  systemd-rpm-macros
# Default pg_dump provider for schema-sync / resharding workflows and
# the default postgres service account expected by the systemd unit.
Requires:       ca-certificates, postgresql18-server, systemd

%description
PgDog is a modern PostgreSQL proxy, pooler, load balancer and query router written in Rust.
This package ships the PgDog daemon, a systemd service unit, default configuration templates.

%prep
%setup -q -n %{sname}-%{version}
mkdir -p packaging/rpm
patch -p1 --forward -f < %{_specdir}/patches/%{sname}.patch || true

%build
if [ "%{_arch}" = "aarch64" ]; then
  export RUSTFLAGS="${RUSTFLAGS:+$RUSTFLAGS }-Ctarget-feature=+lse"
fi
if [ "%{_arch}" = "x86_64" ] && [ -f .cargo/config.toml ]; then
  rm -f .cargo/config.toml
fi
PATH=~/.cargo/bin:$PATH cargo build --release --locked \
  -p pgdog

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

%post
%systemd_post pgdog.service

%preun
%systemd_preun pgdog.service

%postun
%systemd_postun_with_restart pgdog.service

%files
%license LICENSE
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
* Sat Mar 21 2026 Vonng <rh@vonng.com> - 0.1.32-1PIGSTY
- Initial RPM release for PgDog with systemd service and default configuration
