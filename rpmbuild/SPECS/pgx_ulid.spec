%define debug_package %{nil}
%global pname pgx_ulid
%global sname pgx_ulid
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.3
Release:	1PIGSTY%{?dist}
Summary:	ULID type and functions for PostgreSQL
License:	MIT
URL:		https://github.com/pksunkara/%{pname}
SOURCE0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pgx_ulid provides a native ULID type for PostgreSQL together with
generator functions, monotonic generation, and casts to or from UUID
and timestamp values.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}
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
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2.3-1PIGSTY
- https://github.com/pksunkara/pgx_ulid/releases/tag/v0.2.3
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Mon Nov 17 2025 Vonng <rh@vonng.com> - 0.2.2-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.2.1-1PIGSTY
* Tue May 27 2025 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
