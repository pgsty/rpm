%define debug_package %{nil}
%global pname tzf
%global sname pg_tzf
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.4
Release:	1PIGSTY%{?dist}
Summary:	Fast PG extension to lookup timezone name by GPS coordinates
License:	MIT
URL:		https://github.com/ringsaturn/pg-tzf
Source0:	pg-tzf-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Resolve IANA timezone names from longitude/latitude coordinates in PostgreSQL.

%prep
%setup -q -n pg-tzf-%{version}

%build
cd %{_builddir}/pg-tzf-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch
# pgrx 0.17.0 uses NonNull::from_mut(), which is newer than the EL9 Rust
# shipped in our validation container. Rewriting to NonNull::from(&mut ...)
# preserves semantics and keeps the extension buildable on EL9A.
PBOX="$(find "$HOME/.cargo/registry/src" -path '*/pgrx-0.17.0/src/palloc/pbox.rs' | head -n 1)"
test -n "$PBOX"
if ! grep -q 'NonNull::from(\&mut datum)' "$PBOX"; then \
    (cd "$(dirname "$PBOX")" && patch -p0 < %{_specdir}/patches/pgrx-0.17.0-pbox-nonnull.patch); \
fi
cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/pg-tzf-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/pg-tzf-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/pg-tzf-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE LICENSE_DATA
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2.4-1PIGSTY
- https://github.com/ringsaturn/pg-tzf/releases/tag/v0.2.4
- Drop the stale pgvector runtime dependency; upstream now uses PostgreSQL point types
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.2.3
* Thu May 22 2025 Vonng <rh@vonng.com> - 0.2.2
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.2.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
