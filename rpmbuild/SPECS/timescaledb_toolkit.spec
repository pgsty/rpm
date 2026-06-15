%define debug_package %{nil}
%global pname timescaledb_toolkit
%global sname timescaledb-toolkit
%global srcdir timescale-timescaledb-toolkit-845ed35
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:timescaledb_toolkit supports PostgreSQL 15-18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.23.0
Release:	1PIGSTY%{?dist}
Summary:	Extension for more hyperfunctions, fully compatible with TimescaleDB and PostgreSQL
License:	Timescale
URL:		https://github.com/timescale/timescaledb-toolkit
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Recommends: pg_cron_%{pgmajorversion}

%description
Extension for more hyperfunctions, fully compatible with TimescaleDB and PostgreSQL

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{_specdir}/patches/timescaledb-toolkit-1.23.0.patch

%build
cd %{_builddir}/%{srcdir}/extension
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.18.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo update -p pgrx --precise $PGRX_VERSION
cargo update -p pgrx-macros --precise $PGRX_VERSION
cargo update -p pgrx-sql-entity-graph --precise $PGRX_VERSION
cargo update -p pgrx-tests --precise $PGRX_VERSION
cargo fetch

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

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
* Mon Jun 15 2026 Vonng <rh@vonng.com> - 1.23.0-1PIGSTY
- https://github.com/timescale/timescaledb-toolkit/releases/tag/1.23.0
- Patch Cargo metadata to build with cargo-pgrx 0.18.1

* Mon Oct 27 2025 Vonng <rh@vonng.com> - 1.22.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 1.21.0-1PIGSTY
* Thu Jan 23 2025 Vonng <rh@vonng.com> - 1.19.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
