%define debug_package %{nil}
%global pname pg_graphql
%global sname pg_graphql
%global srcdir supabase-pg_graphql-66d4c55
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.6.1
Release:	2PIGSTY%{?dist}
Summary:	GraphQL support to your PostgreSQL database.
License:	Apache-2.0
URL:		https://github.com/supabase/pg_graphql
Source0:	pg_graphql-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_graphql reflects a GraphQL schema from the existing SQL schema.
The extension keeps schema translation and query resolution neatly contained on your database server.
This enables any programming language that can connect to PostgreSQL to query the database via GraphQL with no additional servers, processes, or libraries.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{_specdir}/patches/pg-graphql-1.6.1.patch

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
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo fetch --locked

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

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
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 1.6.1-2PIGSTY
- Migrate the direct-on-pristine source patch and locked pgrx test graph to 0.19.1
- Build offline after locked fetch and reject Cargo.lock rewrites

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 1.6.1-1PIGSTY
- https://github.com/supabase/pg_graphql/releases/tag/v1.6.1
- Patch Cargo metadata to build with cargo-pgrx 0.18.1

* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.5.12-1PIGSTY
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 1.5.11-1PIGSTY
* Thu Oct 17 2024 Vonng <rh@vonng.com> - 1.5.9-1PIGSTY
* Sun Oct 13 2024 Vonng <rh@vonng.com> - 1.5.8-1PIGSTY
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 1.5.7-1PIGSTY
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 1.5.6-1PIGSTY
* Sun May 05 2024 Vonng <rh@vonng.com> - 1.5.4-1PIGSTY
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 1.5.3-1PIGSTY
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 1.5.0-1PIGSTY
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 1.4.4-1PIGSTY
* Wed Oct 11 2023 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
