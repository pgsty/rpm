%define debug_package %{nil}
%global pname pgx_ulid
%global sname pgx_ulid
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgx_ulid only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.3
Release:	3PIGSTY%{?dist}
Summary:	ULID type and functions for PostgreSQL
License:	MIT
URL:		https://github.com/pksunkara/%{pname}
Source0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pgx_ulid provides a native ULID type for PostgreSQL together with
generator functions, monotonic generation, and casts to or from UUID
and timestamp values.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pgx-ulid-0.2.3.patch

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
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
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
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.2.3-3PIGSTY
- Migrate the direct-on-pristine source patch and pgrx/pgrx-tests graph to 0.19.1
- Build offline after locked fetch and reject Cargo.lock rewrites

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.2.3-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2.3-1PIGSTY
- https://github.com/pksunkara/pgx_ulid/releases/tag/v0.2.3
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Mon Nov 17 2025 Vonng <rh@vonng.com> - 0.2.2-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.2.1-1PIGSTY
* Tue May 27 2025 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
