%define debug_package %{nil}
%global pname pg_mooncake
%global sname pg_mooncake
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_mooncake only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	3PIGSTY%{?dist}
Summary:	Columnstore Table in Postgres
License:	MIT
URL:		https://github.com/Mooncake-Labs/pg_mooncake
Source0:    pg_mooncake-%{version}.tar.gz
Patch0:     pg-mooncake-0.2.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server
Requires:   pg_duckdb_%{pgmajorversion} >= 1.1.0

%description
pg_mooncake is a PostgreSQL extension that adds native columnstore tables with DuckDB execution.
Columnstore tables are stored as Iceberg or Delta Lake tables in object storage.
It require pg_duckdb to work.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_EXPECTED=cee79b744de405b5c394f3b45dca765f1db23a9860bbda2d19455be95a24cb3a
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_EXPECTED" ]; then
	echo "unexpected Cargo.lock checksum: $LOCK_BEFORE" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion},bgworker --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/*.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/*.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/*.sql     %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql
%exclude /usr/lib/.build-id/*

%changelog
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
