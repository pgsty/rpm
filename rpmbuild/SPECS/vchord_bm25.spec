%define debug_package %{nil}
%global pname vchord_bm25
%global sname vchord_bm25
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:vchord_bm25 only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.0
Release:	3PIGSTY%{?dist}
Summary:	Native BM25 Ranking Index in PostgreSQL
License:	AGPL-3.0
URL:		https://github.com/supervc-stack/VectorChord-bm25
Source0:	VectorChord-bm25-%{version}.tar.gz
Patch0:		vchord-bm25-0.3.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server pgvector_%{pgmajorversion} >= 0.7.0

%description
A PostgreSQL extension for bm25 ranking algorithm.
We implemented the Block-WeakAnd Algorithms for BM25 ranking inside PostgreSQL.
This extension is currently in alpha stage and not recommended for production use.
We're still iterating on the tokenizer API to support more configurations and languages.
The interface may change in the future.

%prep
%setup -q -n VectorChord-bm25-%{version}
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/VectorChord-bm25-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_EXPECTED=74ee41f8d8cf66ef6f990a39fa8ce5636f2cfaceadcfca6423894c0dd7e8ae9e
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
EXT_DIR=target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension
grep -q "default_version = '%{version}'" ${EXT_DIR}/%{pname}.control
test -f ${EXT_DIR}/%{pname}--%{version}.sql

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/VectorChord-bm25-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/VectorChord-bm25-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/VectorChord-bm25-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.3.0-3PIGSTY
- Build with cargo-pgrx 0.19.1 from a generated, locked dependency graph
- Refresh the source patch and current upstream repository URL

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.3.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Wed Dec 25 2025 Vonng <rh@vonng.com> - 0.3.0
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.2.2
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.2.1
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.1.1
* Mon Feb 10 2025 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
