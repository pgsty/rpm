%define debug_package %{nil}
%global pname pg_typescript
%global sname pg_typescript
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_typescript only supports PostgreSQL 16 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	4PIGSTY%{?dist}
Summary:	TypeScript procedural language extension for PostgreSQL
License:	MIT
URL:		https://github.com/isaacd9/pg_typescript
Source0:	%{sname}-%{version}.tar.gz
#           repacked from upstream tagged snapshot
#           https://github.com/isaacd9/pg_typescript/tree/v0.0.1+414de9491d8f373f829b634d3fe3bbbe0f587ac5
#           because the source tree's Cargo/control version is 0.1.0
Source1:	rusty_v8-149.4.0-simdutf-x86_64-unknown-linux-gnu.a.gz
Source2:	rusty_v8-149.4.0-simdutf-aarch64-unknown-linux-gnu.a.gz
#           unmodified official rusty_v8 v149.4.0 simdutf release archives:
#           https://github.com/denoland/rusty_v8/releases/tag/v149.4.0

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pg_typescript adds a trusted TypeScript procedural language to PostgreSQL,
powered by Deno and V8. It supports TypeScript functions, controlled runtime
permissions, remote import maps, and an API for calling back into PostgreSQL
from TypeScript code.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg-typescript-0.1.0.patch

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')
%ifarch x86_64
export RUSTY_V8_ARCHIVE=%{SOURCE1}
test "$(sha256sum "$RUSTY_V8_ARCHIVE" | awk '{print $1}')" = "aa30f198b6e7be2188df6498f95053c4c052f212037a01f2c31414d7aca84b53"
%else
%ifarch aarch64
export RUSTY_V8_ARCHIVE=%{SOURCE2}
test "$(sha256sum "$RUSTY_V8_ARCHIVE" | awk '{print $1}')" = "54f779336fa85d16ea7950f82d3b8b31326ae09bac84d59763db2c5ceaa0094c"
%else
%{error:pg_typescript rusty_v8 archive is only provided for x86_64 and aarch64}
%endif
%endif
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_SHA256" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during package" >&2
	exit 1
}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{sname}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{sname}-%{version}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.1.0-4PIGSTY
- Embed custom extension ESM and residual lazy Deno sources in the shared library
- Remove runtime reads of cargo build-tree paths from PostgreSQL backends

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.1.0-3PIGSTY
- Build with cargo-pgrx 0.19.1 using the patched, locked dependency graph
- Move to deno_runtime 0.260.0, deno_core 0.405.0, and rusty_v8 149.4.0
  whose official Linux archives support loading from a PostgreSQL shared library

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.1.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Package the upstream pgrx 0.17.0 tagged snapshot for PostgreSQL 16-18
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
