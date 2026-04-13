%define debug_package %{nil}
%global sname postgresql_anonymizer
%global pname anon
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		pg_anon_%{pgmajorversion}
Version:	3.0.13
Release:	1PIGSTY%{?dist}
Summary:	Anonymization & Data Masking for PostgreSQL
License:	PostgreSQL
URL:		https://gitlab.com/dalibo/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#Source0:   https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
postgresql_anonymizer is an extension to mask or replace personally
identifiable information (PII) or commercially sensitive data from a
PostgreSQL database.

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
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension/anon
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/data/*.csv %{buildroot}%{pginstdir}/share/extension/anon/
cp -a %{_builddir}/%{sname}-%{version}/data/en_US %{buildroot}%{pginstdir}/share/extension/anon/
cp -a %{_builddir}/%{sname}-%{version}/data/fr_FR %{buildroot}%{pginstdir}/share/extension/anon/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/extension/anon
%doc README.md AUTHORS.md
%license LICENSE.md
%exclude /usr/lib/.build-id

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 3.0.13-1PIGSTY
- https://gitlab.com/dalibo/postgresql_anonymizer/-/tags/3.0.13
- Switch Source0 to the upstream postgresql_anonymizer tarball name
- Package the locale-specific fake data trees shipped in data/en_US and data/fr_FR
- Drop the stale postgresql-contrib runtime dependency; upstream no longer declares it
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Thu Feb 12 2026 Vonng <rh@vonng.com> - 3.0.1-1PIGSTY
* Tue Feb 10 2026 Vonng <rh@vonng.com> - 3.0.0-1PIGSTY
* Mon Dec 15 2025 Vonng <rh@vonng.com> - 2.5.1-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 2.4.1-1PIGSTY
* Wed Jul 17 2025 Vonng <rh@vonng.com> - 2.3.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 2.1.1-1PIGSTY
* Wed Jan 08 2025 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- Rewrite in Rust
* Wed Oct 11 2023 Vonng <rh@vonng.com> - 1.3.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
