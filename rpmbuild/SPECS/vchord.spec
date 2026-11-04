%global pname vchord
%global sname vchord
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?cargo_target_dir:%global cargo_target_dir %{_builddir}/%{sname}-%{version}/target}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:vchord only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.0
Release:	1PGSTY%{?dist}
Summary:	Scalable, Fast, and Disk-friendly Vector search in Postgres, the Successor of pgvecto.rs.
License:	AGPL-3.0-only
URL:		https://vchord.pgsty.com/
Source0:	vchord-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang >= 16 clang-devel >= 16 rust rustfmt
Requires:	postgresql%{pgmajorversion}-server pgvector_%{pgmajorversion} >= 0.8.0

%description
VectorChord (vchord) is a PostgreSQL extension designed for scalable, high-performance, and disk-efficient vector similarity search, and serves as the successor to pgvecto.rs.

%prep
%setup -q -n vchord-%{version}
# GitHub tag archive: https://github.com/pgsty/vchord/archive/refs/tags/%{version}.tar.gz
# No downstream patch is applied.

%build
%set_build_flags
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
# The ARM64 SIMD C shim requires Clang >= 16 or GCC >= 14. Use Clang for
# every target so the same compiler path is used on EL8, EL9, and EL10.
CLANG_BIN=
for candidate in clang-21 clang-20 clang-19 clang-18 clang-17 clang-16 clang; do
	if command -v "$candidate" >/dev/null 2>&1; then
		CLANG_BIN=$(command -v "$candidate")
		break
	fi
done
if [ -z "$CLANG_BIN" ]; then
	echo "vchord requires clang >= 16" >&2
	exit 1
fi
CLANG_MAJOR=$("$CLANG_BIN" --version | sed -n 's/.*clang version \([0-9][0-9]*\).*/\1/p' | head -1)
case "$CLANG_MAJOR" in
	''|*[!0-9]*)
		echo "unable to determine clang version from $CLANG_BIN" >&2
		exit 1
		;;
esac
if [ "$CLANG_MAJOR" -lt 16 ]; then
	echo "vchord requires clang >= 16, found $CLANG_MAJOR" >&2
	exit 1
fi
CLANGXX_BIN=
for candidate in clang++-21 clang++-20 clang++-19 clang++-18 clang++-17 clang++-16 clang++; do
	if command -v "$candidate" >/dev/null 2>&1; then
		CLANGXX_BIN=$(command -v "$candidate")
		break
	fi
done
if [ -z "$CLANGXX_BIN" ]; then
	CLANGXX_BIN="$CLANG_BIN"
fi
export CC="$CLANG_BIN"
export CXX="$CLANGXX_BIN"
CLANG_LIB="$($CLANG_BIN -print-file-name=libclang.so)"
if [ -f "$CLANG_LIB" ]; then
	export LIBCLANG_PATH="$(cd "$(dirname "$CLANG_LIB")" && pwd -P)"
fi
%if 0%{?rhel} >= 10
export CFLAGS=$(echo "${CFLAGS:-}" | sed -e 's/-flto=auto//g' -e 's/-flto[^ ]*//g' -e 's/-ffat-lto-objects//g')
export CXXFLAGS=$(echo "${CXXFLAGS:-}" | sed -e 's/-flto=auto//g' -e 's/-flto[^ ]*//g' -e 's/-ffat-lto-objects//g')
export LDFLAGS=$(echo "${LDFLAGS:-}" | sed -e 's/-flto=auto//g' -e 's/-flto[^ ]*//g')
%endif
cd %{_builddir}/vchord-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export CARGO_TARGET_DIR=%{cargo_target_dir}

PGRX_VERSION=0.19.3
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_EXPECTED=8d2e52210bcb7daca5643af4ef8ebe703b86451a8bd6a8fddf3c939464ccbb84
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_EXPECTED" ]; then
	echo "unexpected Cargo.lock checksum: $LOCK_BEFORE" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion},simd/init --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi
EXT_DIR=%{cargo_target_dir}/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension
cp -f sql/upgrade/%{pname}--*.sql ${EXT_DIR}/
cp -f sql/install/%{pname}--%{version}.sql ${EXT_DIR}/%{pname}--%{version}.sql
grep -q "default_version = '%{version}'" ${EXT_DIR}/%{pname}.control
test -f ${EXT_DIR}/%{pname}--%{version}.sql

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{cargo_target_dir}/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{cargo_target_dir}/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{cargo_target_dir}/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Nov 04 2026 Vonng <rh@vonng.com> - 1.2.0-1PGSTY
- Switch to the PGSTY-maintained fork and prepare VectorChord 1.2.0
- Build directly from the fork source without a downstream compatibility patch
- Require Clang >= 16 for ARM64 SIMD and preserve compiler debug flags

* Mon Nov 02 2026 Vonng <rh@vonng.com> - 1.1.1-2PGSTY
- Build with cargo-pgrx 0.19.3 and refresh the source patch and locked dependencies

* Sun Sep 06 2026 Vonng <rh@vonng.com> - 1.1.1-1PGSTY
- Build with pgrx 0.19.2 from the updated source archive and locked dependencies

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 1.1.1-3PIGSTY
- Build with cargo-pgrx 0.19.1 from a locked, offline dependency graph
- Refresh the source patch for pgrx 0.19.1 and the current upstream repository

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 1.1.1-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Wed Mar 04 2026 Vonng <rh@vonng.com> - 1.1.1-1PIGSTY
- https://github.com/tensorchord/VectorChord/releases/tag/1.1.1
* Thu Feb 12 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
* Mon Nov 17 2025 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.5.3-1PIGSTY
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 0.5.1-1PIGSTY
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 0.4.3-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.2.2-1PIGSTY
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.2.1-1PIGSTY
* Mon Feb 10 2025 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
