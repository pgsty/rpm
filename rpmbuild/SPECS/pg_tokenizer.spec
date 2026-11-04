%global pname pg_tokenizer
%global sname pg_tokenizer
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_tokenizer only supports PostgreSQL 14 through 18}
%endif

Name:		%{pname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL tokenizer extension for full-text search
License:	Apache-2.0
URL:		https://vchord.pgsty.com/
Source0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang clang-devel rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
A PostgreSQL extension that provides tokenizers for full-text search.

%prep
%setup -q -n %{sname}-%{version}
# GitHub tag archive: https://github.com/pgsty/pg_tokenizer/archive/refs/tags/v%{version}.tar.gz
# No downstream patch is applied.

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.3
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_EXPECTED=4151c42b09d343cc03fb98a4a13e1721b561687b6dd260d90bb7e241ee75fbb6
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
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
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
