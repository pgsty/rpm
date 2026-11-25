%global pname pg_tokenizer
%global sname pg_tokenizer
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?cargo_target_dir:%global cargo_target_dir %{_builddir}/%{sname}-%{version}/target}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:pg_tokenizer only supports PostgreSQL 15 through 19}
%endif

Name:		%{pname}_%{pgmajorversion}
Version:	1.3.0
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL tokenizer extension for full-text search
License:	Apache-2.0
URL:		https://vchord.pgsty.com/
Source0:    %{sname}-%{version}.tar.gz
Patch0:     pg_tokenizer-1.3.0-pgrx-0.20.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang clang-devel rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
A PostgreSQL extension that provides tokenizers for full-text search.

%prep
%setup -q -n %{sname}-%{version}
# GitHub tag archive: https://github.com/pgsty/pg_tokenizer/archive/refs/tags/v%{version}.tar.gz
patch --batch --fuzz=0 -p1 < %{PATCH0}

%build
export RUSTUP_TOOLCHAIN="${RUSTUP_TOOLCHAIN:-1.100.0}"
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export CARGO_TARGET_DIR=%{cargo_target_dir}

PGRX_VERSION=0.20.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_EXPECTED=3bceddee1d0ba553cb11100b2b761d9de5c95b1dfe3b58606ef47bfe38386c4a
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_EXPECTED" ]; then
	echo "unexpected Cargo.lock checksum: $LOCK_BEFORE" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{cargo_target_dir}/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{cargo_target_dir}/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{cargo_target_dir}/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/
install -m 644 sql/upgrade/%{pname}--*--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Nov 25 2026 Vonng <rh@vonng.com> - 1.3.0-1PGSTY
- Update to upstream 1.3.0 with its tokenizer cache and tsvector changes
- Refresh the pgrx 0.20.1 dependency patch and locked checksums

* Mon Nov 23 2026 Vonng <rh@vonng.com> - 1.2.0-1PGSTY
- Build upstream 1.2.0 for PostgreSQL 15 through 19
- Update the locked pgrx and pgrx-tests crates to 0.20.1

* Mon Nov 09 2026 Vonng <rh@vonng.com> - 1.1.0-1PGSTY
- Update to upstream 1.1.0 with tokenizer permission and cache fixes.
- Refresh the upstream Cargo.lock checksum and retain pgrx 0.19.3.

* Wed Nov 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PGSTY
- Switch to the PGSTY-maintained fork and package pg_tokenizer 1.0.0
- Fetch Snowball stemmers from pgsty/rust-stemmers v1.2.1
- Build directly from the fork source without a downstream compatibility patch
- Use the v1.0.0 GitHub source archive with the pg_tokenizer name

* Mon Nov 02 2026 Vonng <rh@vonng.com> - 0.1.1-2PGSTY
- Build with cargo-pgrx 0.19.3 and refresh the source patch and locked dependencies

* Sun Sep 06 2026 Vonng <rh@vonng.com> - 0.1.1-1PGSTY
- Build with pgrx 0.19.2 from the updated source archive and locked dependencies

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.1.1-3PIGSTY
- Build with cargo-pgrx 0.19.1 and a locked dependency graph
- Preserve the PG14-PG18 feature trim and shared-preload linker flags
- Replace the upstream release-workflow version placeholder with 0.1.1

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.1.1-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.1.1
* Mon May 26 2025 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
