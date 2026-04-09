%define debug_package %{nil}
%global pname pg_trickle
%global sname pg_trickle
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_trickle only supports PostgreSQL 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.16.0
Release:	1PIGSTY%{?dist}
Summary:	Streaming tables with differential view maintenance for PostgreSQL 18
License:	Apache-2.0
URL:		https://github.com/grove/pg-trickle
Source0:	%{sname}-%{version}-complete.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pg_trickle turns PostgreSQL 18 into a real-time data platform with streaming
tables and incremental view maintenance, implemented as a pgrx extension.

%prep
%setup -q -n pg_trickle-src
patch -p1 --forward -f < %{_specdir}/patches/pg_trickle-0.16.0-trim-packaging-only-targets.patch

%build
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

# cargo-pgrx is provisioned manually on builders.
cargo pgrx init --pg18=%{pginstdir}/bin/pg_config --no-run
cargo fetch

# pgrx 0.17.0 uses NonNull::from_mut(), which is newer than the EL9 Rust
# toolchain support in this container. Patch the cached crate before building.
PBOX="$(find "$HOME/.cargo/registry/src" -path '*/pgrx-0.17.0/src/palloc/pbox.rs' | head -n 1)"
test -n "$PBOX"
if ! grep -q 'NonNull::from(\&mut datum)' "$PBOX"; then \
    (cd "$(dirname "$PBOX")" && patch -p0 < %{_specdir}/patches/pgrx-0.17.0-pbox-nonnull.patch); \
fi

cargo pgrx package --pg-config %{pginstdir}/bin/pg_config

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/pg_trickle-src/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/pg_trickle-src/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/pg_trickle-src/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Apr 08 2026 Vonng <rh@vonng.com> - 0.16.0-1PIGSTY
- https://github.com/grove/pg-trickle/releases/tag/v0.16.0

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.15.0-1PIGSTY
- Initial RPM release, PG18-only
