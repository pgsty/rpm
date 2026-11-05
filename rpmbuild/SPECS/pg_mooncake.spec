%global pname pg_mooncake
%global sname pg_mooncake
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global cargo_target_dir %{_topdir}/.cache/%{sname}/target
# debugedit recomputes linker Build-IDs; include the PG package name in its seed.
%global _find_debuginfo_opts --build-id-seed %{name}-%{version}-%{release}
%{!?mooncake_jobs:%global mooncake_jobs 4}
%if 0%{?rhel} == 8
%global mooncake_python python3.9
%else
%global mooncake_python python3
%endif

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_mooncake only supports PostgreSQL 14 through 18}
%endif

# RPM's ELF processing removes DuckDB's appended metadata. Restore it only
# after both find-debuginfo and the distribution's normal brp scripts ran.
%global __os_install_post %{__os_install_post} \
for plugin in %{buildroot}%{pginstdir}/share/extension/pg_mooncake/v2.0.0/*/mooncake.duckdb_extension; do \
  if ! tail -c 534 "$plugin" | cmp - %{_builddir}/%{sname}-%{version}/mooncake.footer; then \
    cat %{_builddir}/%{sname}-%{version}/mooncake.footer >> "$plugin"; \
  fi; \
done

Name:       %{sname}_%{pgmajorversion}
Version:    0.3.0
Release:    1PGSTY%{?dist}
Summary:    Real-time columnstore analytics in PostgreSQL
License:    MIT AND BUSL-1.1
URL:        https://github.com/pgsty/pg_mooncake
# v0.3.0 (1a9cbfd65be9a6486d020120acb49ef0c6800d68) plus fetch-deps.sh.
Source0:    pg_mooncake-%{version}.tar.gz

BuildRequires: postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires: cargo rust rustfmt clang-devel llvm-devel
BuildRequires: gcc gcc-c++ make cmake >= 3.24 ninja-build git python3
BuildRequires: pkgconfig openssl-devel libcurl-devel lz4-devel protobuf-compiler
%if 0%{?rhel} == 8
# The version checks require Python 3.9; DuckDB 2.0 needs newer C++ headers.
BuildRequires: python39 gcc-toolset-15-gcc-c++ gcc-toolset-15-annobin-plugin-gcc
%endif
Requires:   postgresql%{pgmajorversion}-server
# The bundled DuckDB extension and SQL guard target exactly DuckDB 2.0.0.
Requires:   pg_duckdb_%{pgmajorversion} = 1.2.0

%description
pg_mooncake adds columnstore tables and real-time replication from PostgreSQL
heap tables, using Moonlink and DuckDB execution. This PGSTY-maintained fork
includes a local DuckDB Mooncake extension for pg_duckdb 1.2.0 / DuckDB 2.0.0.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?rhel} == 8
sed -i 's/python3/python3.9/g' fetch-deps.sh Makefile
%endif
# The small archive deliberately omits dependencies. Fetch only pinned commits.
./fetch-deps.sh
printf '54488fa56bffb86a9d9ee47794ba433c10114ea34ba8e995a3a38709943f9784  Cargo.lock\n' | sha256sum -c -

%build
%set_build_flags
%if 0%{?rhel} == 8
source /opt/rh/gcc-toolset-15/enable
export CC=/opt/rh/gcc-toolset-15/root/usr/bin/gcc
export CXX=/opt/rh/gcc-toolset-15/root/usr/bin/g++
export CFLAGS="$CFLAGS -std=gnu17"
%endif
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
export CARGO_TARGET_DIR=%{cargo_target_dir}
export CARGO_BUILD_JOBS=%{mooncake_jobs}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export DUCKDB_COMMIT=d54cbbe3df17e8e5ce68312f483b4155836112aa
export CARGO_NET_GIT_FETCH_WITH_CLI=true
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
%{mooncake_python} scripts/check_versions.py --check-toolchain
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
chmod 755 %{buildroot}%{pginstdir}/share/extension/pg_mooncake/v2.0.0/*/mooncake.duckdb_extension
mkdir -p licenses
cp LICENSE licenses/pg_mooncake.LICENSE
cp moonlink/LICENSE licenses/moonlink.LICENSE
cp duckdb_mooncake/LICENSE licenses/duckdb_mooncake.LICENSE

%check
for plugin in %{buildroot}%{pginstdir}/share/extension/pg_mooncake/v2.0.0/*/mooncake.duckdb_extension; do
    tail -c 534 "$plugin" | cmp - mooncake.footer
done

%files
%license licenses/*
%doc README.md BUILD.md versions.json
%{pginstdir}/lib/pg_mooncake.so
%{pginstdir}/share/extension/pg_mooncake.control
%{pginstdir}/share/extension/pg_mooncake--%{version}.sql
%{pginstdir}/share/extension/pg_mooncake/

%changelog
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
