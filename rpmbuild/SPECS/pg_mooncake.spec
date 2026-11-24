%global pname pg_mooncake
%global sname pg_mooncake
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global duckdb_version v2.0.1
%global cargo_target_dir %{_topdir}/.cache/%{sname}/target
# debugedit recomputes linker Build-IDs; include the PG package name in its seed.
%global _find_debuginfo_opts --build-id-seed %{name}-%{version}-%{release}
%{!?mooncake_jobs:%global mooncake_jobs 4}
%if 0%{?rhel} && 0%{?rhel} < 9
%{error:pg_mooncake requires Enterprise Linux 9 or newer}
%endif

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:pg_mooncake only supports PostgreSQL 15 through 19}
%endif

# RPM's ELF processing removes DuckDB's appended metadata. Restore it only
# after both find-debuginfo and the distribution's normal brp scripts ran.
%global __os_install_post %{__os_install_post} \
for plugin in %{buildroot}%{pginstdir}/share/extension/pg_mooncake/%{duckdb_version}/*/mooncake.duckdb_extension; do \
  if ! tail -c 534 "$plugin" | cmp - %{_builddir}/%{sname}-%{version}/mooncake.footer; then \
    cat %{_builddir}/%{sname}-%{version}/mooncake.footer >> "$plugin"; \
  fi; \
done

Name:       %{sname}_%{pgmajorversion}
Version:    0.3.4
Release:    1PGSTY%{?dist}
Summary:    Real-time columnstore analytics in PostgreSQL
License:    MIT AND BUSL-1.1
URL:        https://github.com/pgsty/pg_mooncake
Source0:    https://github.com/pgsty/pg_mooncake/releases/download/v%{version}/pg_mooncake-%{version}-source.tar.gz
Patch0:     pg_mooncake-%{version}-pgrx-0.20.1.patch

BuildRequires: postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires: cargo rust rustfmt clang-devel llvm-devel
BuildRequires: gcc gcc-c++ make cmake >= 3.24 ninja-build git python3
BuildRequires: pkgconfig openssl-devel libcurl-devel lz4-devel protobuf-compiler
Requires:   postgresql%{pgmajorversion}-server
Requires:   pg_duckdb_%{pgmajorversion} >= 1.2.1

%description
pg_mooncake adds columnstore tables and real-time replication from PostgreSQL
heap tables, using Moonlink and DuckDB execution. This PGSTY-maintained fork
includes the Mooncake v0.0.5 scanner built for DuckDB 2.0.1.

%prep
%setup -q -n %{sname}-%{version}
patch --batch --fuzz=0 -p1 < %{PATCH0}
echo 'fdf880384b0133105be85cf14527809cb1a1b8a4ab4f7cb9d22464046a22cf23  Cargo.lock' | sha256sum -c -

%build
%set_build_flags
export RUSTUP_TOOLCHAIN="${RUSTUP_TOOLCHAIN:-1.100.0}"
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
export CARGO_TARGET_DIR=%{cargo_target_dir}
export CARGO_BUILD_JOBS=%{mooncake_jobs}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export CARGO_NET_GIT_FETCH_WITH_CLI=true
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
python3 scripts/check_versions.py --check-toolchain
sha256sum Cargo.lock moonlink/Cargo.lock duckdb_mooncake/moonlink_ffi/Cargo.lock > .cargo-locks.before
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked
cargo fetch --locked --manifest-path duckdb_mooncake/moonlink_ffi/Cargo.toml
%{__make} package PG_VERSION=pg%{pgmajorversion} PG_CONFIG=%{pginstdir}/bin/pg_config \
    JOBS=%{mooncake_jobs} PACKAGE_DIR="$PWD/package"
sha256sum -c .cargo-locks.before
tail -c 534 duckdb_mooncake/build/release/extension/mooncake/mooncake.duckdb_extension > mooncake.footer
# RPM 4.20 may remove BUILD after packaging; retain the input footer for QA.
cp mooncake.footer %{cargo_target_dir}/../mooncake.footer

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}
cp -a package%{pginstdir}/. %{buildroot}%{pginstdir}/
# find-debuginfo only considers executable ELF files, including this plugin.
chmod 755 %{buildroot}%{pginstdir}/share/extension/pg_mooncake/%{duckdb_version}/*/mooncake.duckdb_extension
install -m 644 sql/%{sname}--*--*.sql %{buildroot}%{pginstdir}/share/extension/
mkdir -p licenses
cp LICENSE licenses/pg_mooncake.LICENSE
cp moonlink/LICENSE licenses/moonlink.LICENSE
cp duckdb_mooncake/LICENSE licenses/duckdb_mooncake.LICENSE

%check
for plugin in %{buildroot}%{pginstdir}/share/extension/pg_mooncake/%{duckdb_version}/*/mooncake.duckdb_extension; do
    tail -c 534 "$plugin" | cmp - mooncake.footer
done

%files
%license licenses/*
%doc README.md CHANGELOG.md versions.json
%{pginstdir}/lib/pg_mooncake.so
%{pginstdir}/share/extension/pg_mooncake.control
%{pginstdir}/share/extension/pg_mooncake--%{version}.sql
%{pginstdir}/share/extension/pg_mooncake--*--*.sql
%{pginstdir}/share/extension/pg_mooncake/

%changelog
* Tue Nov 24 2026 Vonng <rh@vonng.com> - 0.3.4-1PGSTY
- Require pg_duckdb 1.2.1 or newer and ship the direct upgrades from 0.3.0 through 0.3.3
- Refresh the pgrx 0.20.1 patch for the upstream 0.3.4 source release

* Mon Nov 23 2026 Vonng <rh@vonng.com> - 0.3.3-1PGSTY
- Use the upstream source release with pinned submodules for PostgreSQL 15 through 19
- Update the locked pgrx crates to 0.20.1 and ship the upstream upgrade SQL
- Package scanner v0.0.5 for pg_duckdb 1.2.1 and DuckDB 2.0.1

* Thu Nov 05 2026 Vonng <rh@vonng.com> - 0.3.0-1PGSTY
- Switch to the PGSTY fork with pgrx 0.19.3 and pinned source dependencies
- Package the DuckDB 2.0.0 Mooncake plugin and require pg_duckdb 1.2.0
- Preserve native debug information and the DuckDB metadata footer
- Use Python 3.9 and GCC Toolset 15 on EL8
- Seed debug Build-IDs with the PostgreSQL package name for coinstallation

* Sun Sep 06 2026 Vonng <rh@vonng.com> - 0.2.0-1PGSTY
- Require the matching pg_duckdb 1.1.1 provider package at runtime
- Reuse the platform-local Cargo target tree across PostgreSQL majors

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.2.0-3PIGSTY
- Build with cargo-pgrx 0.19.1 and a locked dependency graph
- Preserve the unpublished 0.2.0 source snapshot and bgworker packaging feature

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.2.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sat Nov 01 2025 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- this is an unpublished release build upon pg_duckdb 1.1.0
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.1.2-1PIGSTY
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 0.1.1-1PIGSTY
* Tue Jan 21 2025 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
* Thu Oct 31 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
