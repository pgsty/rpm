%define debug_package %{nil}
%global pname pgwasm
%global sname pgwasm
%global commit 535b53363f8208af139e757e508e66c46309ee29
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgwasm only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	WebAssembly component runtime for PostgreSQL
License:	BSD-3-Clause
URL:		https://github.com/jnicholls/pgwasm
Source0:	%{sname}-%{version}.tar.gz
# Source0 is the upstream main snapshot at commit 535b53363f8208af139e757e508e66c46309ee29:
# https://github.com/jnicholls/pgwasm/archive/535b53363f8208af139e757e508e66c46309ee29.tar.gz
Patch0:		pgwasm-0.1.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	binutils cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pgwasm runs WebAssembly components inside PostgreSQL and exposes their
exports as strongly typed SQL functions. It uses Wasmtime's component model,
caches compiled modules under PGDATA, and disables WASI capabilities by
default unless a database administrator enables them.

%prep
%setup -q -n %{sname}-%{commit}
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/%{sname}-%{commit}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
rustup target add wasm32-wasip2
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(find . -name Cargo.lock -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
for manifest in pgwasm/tests/guests/*/Cargo.toml; do
	CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked --manifest-path "$manifest"
done
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true \
	cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} \
	--pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(find . -name Cargo.lock -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock files changed during cargo pgrx package" >&2
	exit 1
fi

%check
readelf -Ws target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so | grep -q _PG_init

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/lib
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 0755 target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so \
	%{buildroot}%{pginstdir}/lib/%{pname}.so
%{__install} -m 0644 target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control \
	%{buildroot}%{pginstdir}/share/extension/%{pname}.control
%{__install} -m 0644 target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql \
	%{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%changelog
* Tue Jul 28 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Package upstream snapshot 535b5336 with Wasmtime 44
- Migrate to cargo-pgrx/pgrx 0.19.1 and fix the ARM64 c_char comparison
- Handle PostgreSQL 18 ProcedureCreate and defer backend-only initialization
- Remove dynamic functions through PostgreSQL's dependency-aware deletion path
- Allocate and roll back production shared-memory metric slots
