%define debug_package %{nil}
%global pname pglinter
%global sname pglinter
%global srcdir pmpetit-pglinter-972c06d
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pglinter only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.0
Release:	2PIGSTY%{?dist}
Summary:	PostgreSQL Database Linting and Analysis Extension
License:	PostgreSQL
URL:		https://github.com/pmpetit/pglinter
Source0:	pglinter-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pglinter is a PostgreSQL Database Linting and Analysis Extension that analyzes databases
for potential issues, performance problems, and best practice violations.
This is a Rust conversion of the original Python dblinter tool, providing native
PostgreSQL extension capabilities for database analysis and linting.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{_specdir}/patches/pglinter-2.0.0.patch

%build
cd %{_builddir}/%{srcdir}
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
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 2.0.0-2PIGSTY
- Build with cargo-pgrx 0.19.1 using the patched, locked dependency graph

* Sun Jun 14 2026 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- https://github.com/pmpetit/pglinter/releases/tag/2.0.0
- Patch Cargo metadata to build with cargo-pgrx 0.18.1

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.1.2-1PIGSTY
- https://github.com/pmpetit/pglinter/releases/tag/1.1.2
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Wed Feb 25 2026 Vonng <rh@vonng.com> - 1.1.1-1PIGSTY
- https://github.com/pmpetit/pglinter/releases/tag/1.1.1
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- https://github.com/pmpetit/pglinter/releases/tag/1.1.0
* Mon Dec 15 2025 Vonng <rh@vonng.com> - 1.0.1-1PIGSTY
* Sun Nov 17 2025 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
