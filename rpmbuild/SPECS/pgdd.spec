%define debug_package %{nil}
%global pname pgdd
%global sname pgdd
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgdd only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.6.1
Release:	2PIGSTY%{?dist}
Summary:	PostgreSQL Data Dictionary, Inspect data dictionary via SQL
License:	Apache-2.0
URL:		https://github.com/Vonng/pgdd
Source0:    pgdd-%{version}.tar.gz
#           https://github.com/rustprooflabs/pgdd/archive/refs/tags/0.6.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
The PostgreSQL Data Dictionary (PgDD) is an in-database solution to provide introspection via standard SQL query syntax.
This extension makes it easy to provide a usable data dictionary to all users of a PostgreSQL database.
See the full project documentation: https://rustprooflabs.github.io/pgdd/ for more information.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pgdd-0.6.1.patch

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
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo update -p pgrx --precise $PGRX_VERSION
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

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
* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.6.1-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Mon Dec 15 2025 Vonng <rh@vonng.com> - 0.6.1-1PIGSTY
* Mon Oct 26 2025 Vonng <rh@vonng.com> - 0.6.0-2PIGSTY
- Add PostgreSQL 18 support with pgrx 0.16.1
* Mon May 26 2025 Vonng <rh@vonng.com> - 0.6.0-1PIGSTY
- Add PostgreSQL 17 support with pgrx 0.14.1
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.5.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>