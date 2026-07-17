%define debug_package %{nil}
%global pname pg_durable
%global sname pg_durable
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_durable only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.3
Release:	1PIGSTY%{?dist}
Summary:	Durable SQL functions for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/microsoft/pg_durable
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg-durable-0.2.3.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt openssl-devel pkgconfig
Requires:	postgresql%{pgmajorversion}-server

%description
pg_durable brings durable execution to PostgreSQL, allowing long-running
fault-tolerant functions to be defined in SQL and checkpointed inside the
database. It is implemented as a Rust/pgrx extension with a background worker
and requires loading pg_durable through shared_preload_libraries.

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
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
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
mkdir -p %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{sname}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{sname}-%{version}/LICENSE.txt %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE.txt
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.2.3-1PIGSTY
- Update to upstream pg_durable v0.2.3
- Build with cargo-pgrx 0.19.1 and a migrated, locked dependency graph
- Verify cargo pgrx package does not rewrite Cargo.lock

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.2.2-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sat Jun 06 2026 Vonng <rh@vonng.com> - 0.2.2-1PIGSTY
- Initial RPM release for microsoft/pg_durable v0.2.2
- Patch Cargo.toml to build with cargo-pgrx 0.18.1 for PG14-18
- Keep pgrx 0.18 schema metadata from being garbage-collected by the linker
