%define debug_package %{nil}
%define _build_id_links none

%global commit 8f60b04da47ffefe0e52bda2440134b42874eb75
%global shortcommit 8f60b04
%global protoc_version 25.1
%global neon_libexec %{_libexecdir}/neon
%global neon_pgroot %{_libdir}/neon/pg_install

# The patched PostgreSQL builds are private Neon ABIs.  Do not advertise them
# as system libpq/PostgreSQL providers or resolve their private libraries from
# unrelated system packages.
%global __provides_exclude_from ^%{neon_pgroot}/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$

Name:           neon
Version:        20260525
Release:        2.git%{shortcommit}PGSTY%{?dist}
Summary:        Serverless PostgreSQL storage and compute platform
License:        Apache-2.0 AND PostgreSQL
URL:            https://github.com/neondatabase/neon
Source0:        neon-%{version}.tar.gz
# Snapshot of commit 8f60b04da47ffefe0e52bda2440134b42874eb75,
# including the pinned PostgreSQL 14-17 submodules.
Source1:        protoc-%{protoc_version}-linux-x86_64.zip
# https://github.com/protocolbuffers/protobuf/releases/download/v25.1/protoc-25.1-linux-x86_64.zip
Source2:        neon-cargo-vendor-%{version}.tar.gz
Patch0:         neon-20260525-port-allocation.patch
Patch1:         neon-20260525-packaging.patch
Patch2:         neon-20260525-snapshot-version.patch

# This first package iteration is intentionally scoped to the validated EL9
# x86_64 builder.  Add aarch64 only with its matching protoc asset and build QA.
ExclusiveArch:  x86_64

BuildRequires:  autoconf, automake, bison, cargo >= 1.88, clang, cmake
BuildRequires:  flex, gcc, gcc-c++, git, libcurl-devel, libffi-devel
BuildRequires:  libicu-devel, libseccomp-devel, libtool, make, openssl-devel
BuildRequires:  patchelf
BuildRequires:  perl, pkgconf-pkg-config, protobuf-devel, readline-devel
BuildRequires:  rust >= 1.88, systemd-rpm-macros, unzip, zlib-devel

Requires:       ca-certificates, lsof, openssl, systemd
Requires:       %{name}-compute14%{?_isa} = %{version}-%{release}
Requires:       %{name}-compute15%{?_isa} = %{version}-%{release}
Requires:       %{name}-compute16%{?_isa} = %{version}-%{release}
Requires:       %{name}-compute17%{?_isa} = %{version}-%{release}
Requires(pre):  shadow-utils

%description
Neon is an open-source serverless PostgreSQL platform that separates compute
from storage.  This package contains the pageserver, safekeeper, storage
broker, storage controller, local control-plane CLI, compute controller,
proxy, and storage maintenance tools.  The matching compute subpackages ship
Neon's private patched PostgreSQL 14 through 17 distributions.

The neon_local control plane is intended for development, testing, and
small self-hosted experiments.  Neon's production cloud control plane is not
part of the open-source repository.

%package compute14
Summary:        Neon patched PostgreSQL 14 compute runtime

%description compute14
Private PostgreSQL 14 runtime and Neon storage extensions used by Neon compute
nodes.  It is installed below %{neon_pgroot}/v14 and does not replace PGDG
PostgreSQL packages.

%package compute15
Summary:        Neon patched PostgreSQL 15 compute runtime

%description compute15
Private PostgreSQL 15 runtime and Neon storage extensions used by Neon compute
nodes.  It is installed below %{neon_pgroot}/v15 and does not replace PGDG
PostgreSQL packages.

%package compute16
Summary:        Neon patched PostgreSQL 16 compute runtime

%description compute16
Private PostgreSQL 16 runtime and Neon storage extensions used by Neon compute
nodes.  It is installed below %{neon_pgroot}/v16 and does not replace PGDG
PostgreSQL packages.

%package compute17
Summary:        Neon patched PostgreSQL 17 compute runtime

%description compute17
Private PostgreSQL 17 runtime and Neon storage extensions used by Neon compute
nodes.  It is installed below %{neon_pgroot}/v17 and does not replace PGDG
PostgreSQL packages.

%prep
%autosetup -p1 -n %{name}-%{version}

# Cargo.lock contains both crates.io and git dependencies.  Source2 is the
# exact cargo vendor output for this snapshot; merge its source replacement
# into the project config so every Cargo invocation is offline.
tar -xzf %{SOURCE2}
test -d cargo-vendor/vendor
test -s cargo-vendor/config.toml
cat cargo-vendor/config.toml >> .cargo/config.toml

mkdir -p .protoc
unzip -q %{SOURCE1} -d .protoc
test "$(.protoc/bin/protoc --version)" = "libprotoc %{protoc_version}"

%build
cd %{_builddir}/%{name}-%{version}

# Use EL's packaged Rust toolchain.  The upstream snapshot pins Rust 1.88.0;
# newer compilers are supported and the actual versions are recorded in logs.
export PATH=$PWD/.protoc/bin:/usr/bin:/bin
unset RUSTUP_HOME RUSTUP_TOOLCHAIN
export CARGO_HOME=$PWD/.cargo-home
export CARGO_NET_OFFLINE=true
export GIT_VERSION=%{commit}
export BUILD_TAG=%{version}-%{release}

rustc --version
cargo --version
protoc --version

LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo fetch --locked --offline

BUILD_TYPE=release \
CARGO_BUILD_FLAGS="--locked --offline" \
%{__make} %{?_smp_mflags} -s

LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
  echo "Cargo.lock changed during the Neon build" >&2
  exit 1
fi

%install
%{__rm} -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{neon_libexec}
install -d %{buildroot}%{neon_pgroot}
install -d %{buildroot}%{_unitdir}
install -d -m 0750 %{buildroot}%{_localstatedir}/lib/neon

for binary in \
  compute_ctl \
  endpoint_storage \
  neon_local \
  pagectl \
  pageserver \
  pg_sni_router \
  proxy \
  safekeeper \
  storage_broker \
  storage_controller \
  storage_scrubber \
  storcon_cli
do
  install -pm 0755 target/release/${binary} %{buildroot}%{neon_libexec}/${binary}
done

install -pm 0755 packaging/rpm/neon %{buildroot}%{_bindir}/neon
ln -s neon %{buildroot}%{_bindir}/neon_local
install -pm 0644 packaging/rpm/neon-local.service %{buildroot}%{_unitdir}/neon-local.service

for pgversion in 14 15 16 17; do
  install -d %{buildroot}%{neon_pgroot}/v${pgversion}
  cp -a pg_install/v${pgversion}/. %{buildroot}%{neon_pgroot}/v${pgversion}/

  # PostgreSQL/PGXS records the temporary build prefix in executable and
  # extension RUNPATHs.  Make every such ELF resolve libraries from its own
  # private, relocatable Neon distribution.
  find %{buildroot}%{neon_pgroot}/v${pgversion}/bin \
       %{buildroot}%{neon_pgroot}/v${pgversion}/lib -type f | while read elf; do
    old_rpath=$(patchelf --print-rpath "${elf}" 2>/dev/null || true)
    case "${old_rpath}" in
      *%{_builddir}*)
        case "${elf}" in
          */bin/*)            new_rpath='$ORIGIN/../lib' ;;
          */lib/postgresql/*) new_rpath='$ORIGIN/..' ;;
          */lib/*)            new_rpath='$ORIGIN' ;;
          *) echo "unexpected Neon ELF path: ${elf}" >&2; exit 1 ;;
        esac
        patchelf --set-rpath "${new_rpath}" "${elf}"
        ;;
    esac
  done
done

%check
cd %{_builddir}/%{name}-%{version}
target/release/neon_local --version | grep -F 'git-env:%{commit}'
target/release/pageserver --version | grep -F 'git-env:%{commit}'
target/release/safekeeper --version | grep -F 'git-env:%{commit}'
for pgversion in 14 15 16 17; do
  pg_install/v${pgversion}/bin/postgres --version
  test -f pg_install/v${pgversion}/lib/postgresql/neon.so

  neon_so=%{buildroot}%{neon_pgroot}/v${pgversion}/lib/postgresql/neon.so
  test "$(patchelf --print-rpath "${neon_so}")" = '$ORIGIN/..'
  neon_libpq=$(ldd "${neon_so}" | awk '/libpq[.]so[.]5 =>/ { print $3 }')
  test "$(realpath "${neon_libpq}")" = \
    "$(realpath %{buildroot}%{neon_pgroot}/v${pgversion}/lib/libpq.so.5)"
  test "$(patchelf --print-rpath \
    %{buildroot}%{neon_pgroot}/v${pgversion}/bin/psql)" = '$ORIGIN/../lib'
  psql_libpq=$(ldd %{buildroot}%{neon_pgroot}/v${pgversion}/bin/psql | \
    awk '/libpq[.]so[.]5 =>/ { print $3 }')
  test "$(realpath "${psql_libpq}")" = \
    "$(realpath %{buildroot}%{neon_pgroot}/v${pgversion}/lib/libpq.so.5)"

  if find %{buildroot}%{neon_pgroot}/v${pgversion}/bin \
          %{buildroot}%{neon_pgroot}/v${pgversion}/lib -type f | \
     while read elf; do
       patchelf --print-rpath "${elf}" 2>/dev/null || true
     done | grep -F '%{_builddir}'; then
    echo "temporary build RUNPATH remains in PostgreSQL ${pgversion}" >&2
    exit 1
  fi
done

%pre
if ! getent group neon >/dev/null 2>&1; then
  groupadd -r neon
fi
if ! getent passwd neon >/dev/null 2>&1; then
  useradd -r -g neon -d %{_localstatedir}/lib/neon -s /sbin/nologin \
    -c "Neon Serverless PostgreSQL" neon
fi

%post
%systemd_post neon-local.service

%preun
%systemd_preun neon-local.service

%postun
%systemd_postun_with_restart neon-local.service

%files
%license LICENSE
%doc NOTICE README.md
%{_bindir}/neon
%{_bindir}/neon_local
%{_unitdir}/neon-local.service
%dir %{_libexecdir}/neon
%{_libexecdir}/neon/*
%dir %{_libdir}/neon
%dir %{neon_pgroot}
%dir %attr(0750,neon,neon) %{_localstatedir}/lib/neon

%files compute14
%license vendor/postgres-v14/COPYRIGHT
%{neon_pgroot}/v14

%files compute15
%license vendor/postgres-v15/COPYRIGHT
%{neon_pgroot}/v15

%files compute16
%license vendor/postgres-v16/COPYRIGHT
%{neon_pgroot}/v16

%files compute17
%license vendor/postgres-v17/COPYRIGHT
%{neon_pgroot}/v17

%changelog
* Mon Aug 24 2026 Vonng <rh@vonng.com> - 20260525-2.git8f60b04PGSTY
- Vendor the locked Cargo graph and make the RPM build fully offline
- Make the SRPM self-contained by declaring all three packaging patches
- Use each compute runtime's private libpq through a relative RUNPATH
- Rewrite all private PostgreSQL ELF RUNPATHs to relocatable $ORIGIN paths

* Mon Aug 24 2026 Vonng <rh@vonng.com> - 20260525-1.git8f60b04PGSTY
- Package Neon snapshot 8f60b04 with PostgreSQL 14 through 17 runtimes
- Use upstream protoc 25.1 and a locked Cargo dependency graph
- Add the local control-plane wrapper, systemd unit, and endpoint port fix
