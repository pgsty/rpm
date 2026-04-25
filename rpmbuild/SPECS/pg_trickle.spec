%define debug_package %{nil}
%global pname pg_trickle
%global sname pg_trickle
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_trickle only supports PostgreSQL 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.31.0
Release:	1PIGSTY%{?dist}
Summary:	Streaming tables with differential view maintenance for PostgreSQL 18
License:	Apache-2.0
URL:		https://github.com/grove/pg-trickle
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_trickle/0.31.0/pg_trickle-0.31.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pg_trickle turns PostgreSQL 18 into a real-time data platform with streaming
tables and incremental view maintenance, implemented as a pgrx extension.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}.patch

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.18.0
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	cargo install --locked cargo-pgrx --version "$PGRX_VERSION"
fi
cargo pgrx init --pg18=%{pginstdir}/bin/pg_config --no-run
cargo fetch

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
cargo pgrx package --pg-config %{pginstdir}/bin/pg_config

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
mkdir -p %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
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
* Sat Apr 25 2026 Vonng <rh@vonng.com> - 0.31.0-1PIGSTY
- Update to upstream PGXN 0.31.0 with the normalized source tarball
- Refresh the packaging-only Cargo patch for pgrx 0.18.0 and the expanded workspace
- Keep pgrx 0.18 schema metadata from being garbage-collected by the linker

* Fri Apr 17 2026 Vonng <rh@vonng.com> - 0.20.0-1PIGSTY
- Update to upstream 0.20.0 with the normalized PGXN source bundle
- Refresh the packaging-only Cargo target trim patch for the expanded bench set
- Keep patching cached pgrx 0.17.0 to avoid the Rust toolchain
  NonNull::from_mut incompatibility on the current EL builders

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.17.0-1PIGSTY
- Update to upstream 0.17.0 with the normalized pg_trickle-0.17.0.tar.gz source tarball
- Keep trimming the non-extension workspace/test targets for EL9A package builds
- Keep patching cached pgrx 0.17.0 to avoid the Rust toolchain
  NonNull::from_mut incompatibility on the current EL9A builders

* Wed Apr 08 2026 Vonng <rh@vonng.com> - 0.16.0-1PIGSTY
- https://github.com/grove/pg-trickle/releases/tag/v0.16.0

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.15.0-1PIGSTY
- Initial RPM release, PG18-only
