%global pname vchord_bm25
%global sname vchord_bm25
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?cargo_target_dir:%global cargo_target_dir %{_builddir}/%{sname}-%{version}/target}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:vchord_bm25 only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PGSTY%{?dist}
Summary:	Native BM25 Ranking Index in PostgreSQL
License:	AGPL-3.0-only
URL:		https://vchord.pgsty.com/
Source0:	vchord_bm25-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang clang-devel rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
A PostgreSQL extension for BM25 ranking over PostgreSQL tsvector values, using
the Block-WeakAnd (WAND) algorithm. It can use standard PostgreSQL text search
configurations and optionally integrate with pg_tokenizer.
Version 1.0.0 is the first PGSTY release. It uses PostgreSQL tsvector values
and a new index format that is not compatible with upstream 0.3.0 indexes.

%prep
%setup -q -n vchord_bm25-%{version}
# GitHub tag archive: https://github.com/pgsty/vchord_bm25/archive/refs/tags/%{version}.tar.gz
# No downstream patch is applied.

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/vchord_bm25-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export CARGO_TARGET_DIR=%{cargo_target_dir}

PGRX_VERSION=0.19.3
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_EXPECTED=332f2ea12e66ead36e59d6a8592d69e48b84c8c42233e46cc2d743ed9976cc40
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_EXPECTED" ]; then
	echo "unexpected Cargo.lock checksum: $LOCK_BEFORE" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true CARGO_NET_OFFLINE=true cargo pgrx package -v --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
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
* Wed Nov 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PGSTY
- Switch to the PGSTY-maintained fork and prepare VectorChord-bm25 1.0.0
- Use PostgreSQL tsvector values and the new PGSTY index format
- Build directly from the fork source without a downstream compatibility patch
- Install the fork's release SQL and supplied upgrade scripts

* Mon Nov 02 2026 Vonng <rh@vonng.com> - 0.3.0-2PGSTY
- Build with cargo-pgrx 0.19.3 and refresh the source patch and locked dependencies

* Sun Sep 06 2026 Vonng <rh@vonng.com> - 0.3.0-1PGSTY
- Build with pgrx 0.19.2 from the updated source archive and locked dependencies

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.3.0-3PIGSTY
- Build with cargo-pgrx 0.19.1 from a generated, locked dependency graph
- Refresh the source patch and current upstream repository URL

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.3.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Thu Dec 25 2025 Vonng <rh@vonng.com> - 0.3.0
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.2.2
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.2.1
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.1.1
* Mon Feb 10 2025 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
