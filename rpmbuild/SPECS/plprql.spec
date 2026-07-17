%define debug_package %{nil}
%global pname plprql
%global sname plprql
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:plprql only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	18.0.1
Release:	3PIGSTY%{?dist}
Summary:	Use PRQL in PostgreSQL
License:	Apache-2.0
URL:		https://github.com/kaspermarstal/plprql
Source0:    plprql-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
PL/PRQL is a PostgreSQL extension that lets you write functions with PRQL. The extension supports PostgreSQL v14-18 on Linux and macOS.

PRQL (Pipelined Relational Query Language) is an open source query language for data manipulation and analysis that compiles to SQL.
PRQL introduces a pipeline concept (similar to Unix pipes) that transforms data line-by-line. The sequential series of transformations
 reduces the complexity often encountered with nested SQL queries and makes your data manipulation logic easier to read and write.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/plprql-18.0.1.patch

%build
WORKSPACE_ROOT=%{_builddir}/%{sname}-%{version}
cd "$WORKSPACE_ROOT"
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum "$WORKSPACE_ROOT/Cargo.lock" | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
cd "$WORKSPACE_ROOT/%{pname}"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum "$WORKSPACE_ROOT/Cargo.lock" | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during package: $LOCK_BEFORE -> $LOCK_AFTER" >&2
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
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 18.0.1-3PIGSTY
- Build with cargo-pgrx 0.19.1 from a locked workspace dependency graph
- Correct the upstream release archive's crate versions from 18.0.0 to 18.0.1

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 18.0.1-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Tue Feb 10 2026 Vonng <rh@vonng.com> - 18.0.1-1PIGSTY
* Wed Oct 29 2025 Vonng <rh@vonng.com> - 18.0.0-1PIGSTY
* Sun May 05 2024 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
