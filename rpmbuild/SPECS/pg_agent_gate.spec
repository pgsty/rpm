%global pname pg_agent_gate
%global sname pg_agent_gate
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global pgrx_version 0.19.3

%if 0%{?pgmajorversion} != 18
%{error:pg_agent_gate is packaged for PostgreSQL 18 only}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.4.1
Release:        1PGSTY%{?dist}
Summary:        Server-side SQL proposal and approval gate for agent roles
License:        Apache-2.0
URL:            https://github.com/Manuelreyesbravo/pg_agent_gate
Source0:        %{sname}-%{version}.tar.gz
# https://github.com/Manuelreyesbravo/pg_agent_gate/archive/refs/tags/v0.4.1.tar.gz
# SHA256: fae0bff41e71f5f6462745477800c334a7cbf043953aaf862de81dd42076ec36
# Upstream pins pgrx 0.19.2 but omits Cargo.lock. Use the builder's pgrx 0.19.3
# with a fixed dependency graph, and explicitly select pg18 instead of pg19.
Patch0:         pg-agent-gate-0.4.1-pgrx-0.19.3.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
Verify and execute SQL proposals under an agent role's own privileges, record
attempts and optionally require human approval before committing proposals.
The library must be loaded before the agent's first statement via shared or
role-level session preload. The package does not change server configuration.
Optional bound assertions use the separate pg_living_assertions extension.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "%{pgrx_version}" ]; then
    echo "cargo-pgrx %{pgrx_version} is required; run pig build pgrx -v %{pgrx_version} before building" >&2
    exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
PKGDIR=target/release/%{pname}-pg%{pgmajorversion}%{pginstdir}
cp -a "$PKGDIR/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR/share/extension/"* %{buildroot}%{pginstdir}/share/extension/
# Preserve the supplied SQL updates; cargo-pgrx generates the base install SQL.
cp -a sql/%{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id

%changelog
* Tue Nov 03 2026 Vonng <rh@vonng.com> - 0.4.1-1PGSTY
- Update to 0.4.1 with agent-role membership escape fixes.
- Retain the pinned pgrx 0.19.3 dependency graph and full debug output.

* Wed Oct 28 2026 Ruohang Feng <rh@vonng.com> - 0.3.0-1PGSTY
- Initial RPM release for PostgreSQL 18.
- Pin pgrx 0.19.3 and a shared Cargo.lock for reproducible builds.
- Preserve upstream SQL updates and full release debug information.
