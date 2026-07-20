%define debug_package %{nil}
%global pname oidc_validator
%global sname pg_oidc_validator
%global commit b65bbbe288f84fab91d58b8304e8a526d1326af5
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_oidc_validator only supports PostgreSQL 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	OIDC bearer-token validator for PostgreSQL 18
License:	LicenseRef-Upstream-No-License
URL:		https://github.com/UnAfraid/pg_oidc_validator_rust
Source0:	%{sname}-%{version}.tar.gz
# Source0 is the upstream master snapshot at commit b65bbbe288f84fab91d58b8304e8a526d1326af5:
# https://github.com/UnAfraid/pg_oidc_validator_rust/archive/b65bbbe288f84fab91d58b8304e8a526d1326af5.tar.gz
Patch0:		pg-oidc-validator-0.1.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang-devel openssl-devel rust rustfmt
BuildRequires:	binutils
Requires:	postgresql%{pgmajorversion}-server

%description
pg_oidc_validator provides an OIDC bearer-token validator module for the
PostgreSQL 18 OAuth authentication mechanism. It performs OIDC discovery,
fetches the issuer JWKS, validates JWT access tokens, and returns the token
subject as the authenticated identity. Configure PostgreSQL with
oauth_validator_libraries = 'oidc_validator' to load the module.

%prep
%setup -q -n pg_oidc_validator_rust-%{commit}
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/pg_oidc_validator_rust-%{commit}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
PG_CONFIG=%{pginstdir}/bin/pg_config CARGO_NET_OFFLINE=true \
	cargo build --release --locked --no-default-features --features pg18
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo build" >&2
	exit 1
fi

%check
readelf -Ws target/release/lib%{pname}.so | grep -q _PG_oauth_validator_module_init

%install
%{__rm} -rf %{buildroot}
%{__install} -D -m 0755 target/release/lib%{pname}.so \
	%{buildroot}%{pginstdir}/lib/%{pname}.so

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so

%changelog
* Mon Jul 20 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Package upstream snapshot b65bbbe for the PostgreSQL 18 OAuth validator API
- Build with cargo-pgrx/pgrx 0.19.1 and a fixed Cargo.lock
