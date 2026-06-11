%define debug_package %{nil}
%global pname pg_durable
%global sname pg_durable
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_durable only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.2
Release:	1PIGSTY%{?dist}
Summary:	Durable SQL functions for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/microsoft/pg_durable
Source0:	%{sname}-%{version}.tar.gz

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
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}-pgrx-0.18.1.patch

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.18.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch

# pgrx 0.18 embeds extension schema metadata in a linker section; without this
# flag the EL9A linker can garbage-collect it and cargo-pgrx reports a missing
# .pgrxsc section during packaging.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

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
* Sat Jun 06 2026 Vonng <rh@vonng.com> - 0.2.2-1PIGSTY
- Initial RPM release for microsoft/pg_durable v0.2.2
- Patch Cargo.toml to build with cargo-pgrx 0.18.1 for PG14-18
- Keep pgrx 0.18 schema metadata from being garbage-collected by the linker
