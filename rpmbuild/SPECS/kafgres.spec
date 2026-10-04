%global pname kafgres
%global sname kafgres
%global srcdir kafgres-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 16
%{error:PGSTY builds kafgres 0.3.0 for PostgreSQL 16}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.0
Release:	1PGSTY%{?dist}
Summary:        Kafka protocol broker embedded in PostgreSQL
License:	Elastic-2.0
URL:		https://github.com/RayElg/kafgres
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/RayElg/kafgres/archive/refs/tags/0.3.0.tar.gz
# Build the unmodified upstream release with its committed Cargo.lock.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
kafgres embeds a Kafka protocol broker in PostgreSQL, with SQL-managed
topics, partitions and message production. It requires shared_preload_libraries
and a server restart. The default segment engine stores its message log in
separate files and needs its own replication and archive configuration.
The table engine stores the message log in PostgreSQL tables.

%prep
%setup -q -n %{srcdir}
find . -type f -name '._*' -delete

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}/extension
export PATH=%{pginstdir}/bin:${PGRX_BIN_DIR:-$HOME/.cargo/bin}:$PATH

PGRX_VERSION=0.16.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo fetch --locked

CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_BEFORE" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
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
install -m 644 %{_builddir}/%{srcdir}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 0.3.0-1PGSTY
- Update to 0.3.0.

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Package upstream 0.1.0 with the original pgrx 0.16.1 lockfile
- Retain full Rust DWARF for debuginfo and debugsource packages
