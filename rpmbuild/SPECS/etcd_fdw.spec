%define debug_package %{nil}
%global pname etcd_fdw
%global sname etcd_fdw
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	1PIGSTY%{?dist}
Summary:	Foreign data wrapper for etcd
License:	MIT
URL:		https://github.com/cybertec-postgresql/etcd_fdw
Source0:	etcd_fdw-%{version}.tar.gz
Source1:	wrappers-0.6.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	protobuf-compiler
Requires:	postgresql%{pgmajorversion}-server

%description
etcd_fdw is a PostgreSQL foreign data wrapper for etcd,
the distributed key-value store used for shared configuration and service discovery.

%prep
%setup -q -n %{srcdir}
mkdir -p vendor/wrappers
tar -C vendor/wrappers --strip-components=1 -xf %{SOURCE1}
patch -p1 --forward -f < %{_specdir}/patches/etcd-fdw-0.0.1.patch

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.18.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo update -p pgrx@$PGRX_VERSION --precise $PGRX_VERSION
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo update -p pgrx-tests@$PGRX_VERSION --precise $PGRX_VERSION
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sun Jun 14 2026 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Upgrade to upstream 0.0.1
- Vendor wrappers 0.6.1 and patch Cargo metadata for cargo-pgrx 0.18.1

* Sat Jan 17 2026 Vonng <rh@vonng.com> - 0.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
