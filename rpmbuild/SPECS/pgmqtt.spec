%define debug_package %{nil}
%global pname pgmqtt
%global sname pgmqtt
%global srcdir pgmqtt-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgmqtt supports PostgreSQL 14-18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.4.1
Release:	1PIGSTY%{?dist}
Summary:	CDC-to-MQTT broker extension for PostgreSQL
License:	Elastic-2.0
URL:		https://github.com/RayElg/pgmqtt
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/RayElg/pgmqtt/archive/refs/tags/0.4.1.tar.gz
Patch0:		pgmqtt-0.4.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang
Requires:	postgresql%{pgmajorversion}-server

%description
pgmqtt is a PostgreSQL extension that embeds an MQTT broker and bridges table
change events to MQTT topics through SQL-configured CDC mappings. The extension
uses logical decoding under the hood, so wal_level must be configured for
logical replication when it is deployed.

%prep
%setup -q -n %{srcdir}
find . -type f -name '._*' -delete
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/%{srcdir}/extension
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
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
cp -a %{_builddir}/%{srcdir}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{srcdir}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{srcdir}/LICENSE.md %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.4.1-1PIGSTY
- Update to upstream 0.4.1 and add a committed pgrx 0.19.1 Cargo.lock

* Sun Jun 14 2026 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Package upstream release 0.3.0 for PostgreSQL 14-18
- Patch Cargo metadata to build with cargo-pgrx 0.18.1

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Package upstream release 0.1.0 for PostgreSQL 13-18
- Build the pgrx extension from the repository's extension/ subdirectory
- Build with cargo-pgrx 0.17.0 after patching the upstream Cargo manifest
