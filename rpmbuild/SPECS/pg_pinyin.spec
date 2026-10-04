%global pname pg_pinyin
%global sname pg_pinyin
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_pinyin only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.8
Release:	1PGSTY%{?dist}
Summary:	Pinyin romanization and search helpers for PostgreSQL
License:	MIT
URL:		https://github.com/aiyou178/pg_pinyin
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/aiyou178/pg_pinyin/archive/refs/tags/v0.0.8.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
Pinyin romanization and search helpers for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

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
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
EXT_DIR=target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension
cp -f %{pname}--*.sql "$EXT_DIR/"
test "$LOCK_SHA256" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during package" >&2
	exit 1
}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc readme.md README.zh-CN.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 0.0.8-1PGSTY
- Update to 0.0.8.

* Tue Sep 01 2026 Vonng <rh@vonng.com> - 0.0.6-1PGSTY
- Update to upstream v0.0.6 with native pgrx 0.19.2 and PostgreSQL 14-18 support
- Keep the locked dependency graph and declare the pgrx 0.19.2 Rust 1.96 MSRV
- Ship the complete 0.0.2 through 0.0.6 extension upgrade chain

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.0.5-1PIGSTY
- Update to upstream v0.0.5 with native pgrx 0.19.1 support
- Declare the pgrx 0.19 MSRV and build from the committed Cargo.lock

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.0.4-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 0.0.4-1PIGSTY
- Update to upstream v0.0.4
- Patch Cargo.toml to build with cargo-pgrx 0.18.1 for PG14-18

* Wed Mar 04 2026 Vonng <rh@vonng.com> - 0.0.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
