%define debug_package %{nil}
%global pname pg_strict
%global sname pg_strict
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_strict only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.5
Release:	3PIGSTY%{?dist}
Summary:	A PostgreSQL extension to prevent dangerous UPDATE and DELETE without WHERE clause
License:	MIT
URL:		https://github.com/spa5k/pg_strict
Source0:    pg_strict-%{version}.tar.gz
#           https://github.com/spa5k/pg_strict/archive/refs/tags/v1.0.5.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pg_strict is a PostgreSQL extension that prevents dangerous UPDATE and DELETE
statements by requiring a WHERE clause. It enforces rules at parse/analyze time
and provides configurable GUC settings (pg_strict.require_where_on_update and
pg_strict.require_where_on_delete) with three modes: off, warn, and on.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg-strict-1.0.5.patch

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
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 1.0.5-3PIGSTY
- Migrate the direct-on-pristine source patch and fixed dependency graph to pgrx 0.19.1
- Build offline after locked fetch and reject Cargo.lock rewrites

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 1.0.5-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.0.5-1PIGSTY
- https://github.com/spa5k/pg_strict/releases/tag/v1.0.5
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Wed Feb 18 2026 Vonng <rh@vonng.com> - 1.0.3-1PIGSTY
- https://github.com/spa5k/pg_strict/releases/tag/v1.0.3
* Thu Feb 12 2026 Vonng <rh@vonng.com> - 1.0.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
