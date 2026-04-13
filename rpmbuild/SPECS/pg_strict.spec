%define debug_package %{nil}
%global pname pg_strict
%global sname pg_strict
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.5
Release:	1PIGSTY%{?dist}
Summary:	A PostgreSQL extension to prevent dangerous UPDATE and DELETE without WHERE clause
License:	MIT
URL:		https://github.com/spa5k/pg_strict
SOURCE0:    pg_strict-%{version}.tar.gz
#           https://github.com/spa5k/pg_strict/archive/refs/tags/v1.0.5.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_strict is a PostgreSQL extension that prevents dangerous UPDATE and DELETE
statements by requiring a WHERE clause. It enforces rules at parse/analyze time
and provides configurable GUC settings (pg_strict.require_where_on_update and
pg_strict.require_where_on_delete) with three modes: off, warn, and on.

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
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.0.5-1PIGSTY
- https://github.com/spa5k/pg_strict/releases/tag/v1.0.5
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Wed Feb 18 2026 Vonng <rh@vonng.com> - 1.0.3-1PIGSTY
- https://github.com/spa5k/pg_strict/releases/tag/v1.0.3
* Thu Feb 12 2026 Vonng <rh@vonng.com> - 1.0.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
