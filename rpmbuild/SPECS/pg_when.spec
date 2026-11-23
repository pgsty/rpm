%global pname pg_when
%global sname pg_when
%global srcdir pg-when-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:pg_when requires PostgreSQL 15 through 19}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.11
Release:	1PGSTY%{?dist}
Summary:	Natural-language timestamp parser for PostgreSQL
License:	MIT
URL:		https://github.com/frectonz/pg-when
# https://github.com/frectonz/pg-when/archive/refs/tags/0.1.11.tar.gz
# SHA256: 5a89640bbfaa3ab06fccf4c2ccb34865ef1663490c88ad96d1f9d0fa0c8ab5cd
Source0:	%{sname}-%{version}.tar.gz
Patch0:         pg-when-0.1.11-pgrx-0.20.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pg_when parses natural-language date, time, and timezone expressions directly
inside PostgreSQL. It exposes timestamptz and Unix-epoch helper functions for
phrases such as "next friday at 8:00 pm in America/New_York".

%prep
%setup -q -n %{srcdir}

%patch -P0 -p1

%build
export RUSTUP_TOOLCHAIN="${RUSTUP_TOOLCHAIN:-1.100.0}"
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.20.1
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
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{srcdir}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Nov 23 2026 Ruohang Feng <rh@vonng.com> - 0.1.11-1PGSTY
- Build with pgrx and cargo-pgrx 0.20.1 on Rust 1.100.0.
- Update to upstream 0.1.11 and build for PostgreSQL 15 through 19 with pgrx 0.20.0.

* Sun Sep 06 2026 Vonng <rh@vonng.com> - 0.1.10-1PGSTY
- Build with pgrx 0.19.2 from the updated source archive and locked dependencies

* Fri Aug 14 2026 Vonng <rh@vonng.com> - 0.1.10-1PGSTY
- Update to upstream PGXN 0.1.10
- Build with cargo-pgrx 0.19.1 using the patched, locked dependency graph

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.1.9-3PIGSTY
- Build with cargo-pgrx 0.19.1 using the patched, locked dependency graph

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.1.9-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.1.9-1PIGSTY
- Package upstream tag 0.1.9 for PostgreSQL 13-18
- Build with cargo-pgrx 0.17.0 after patching the upstream Cargo manifest
