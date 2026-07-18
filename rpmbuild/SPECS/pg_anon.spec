%define debug_package %{nil}
%global sname postgresql_anonymizer
%global pname anon
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_anon supports PostgreSQL 14 through 18}
%endif

Name:		pg_anon_%{pgmajorversion}
Version:	3.1.3
Release:	2PIGSTY%{?dist}
Summary:	Anonymization & Data Masking for PostgreSQL
License:	PostgreSQL
URL:		https://gitlab.com/dalibo/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#           https://gitlab.com/dalibo/postgresql_anonymizer/-/archive/3.1.3/postgresql_anonymizer-3.1.3.tar.gz
Patch0:		pg-anon-3.1.3.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
postgresql_anonymizer is an extension to mask or replace personally
identifiable information (PII) or commercially sensitive data from a
PostgreSQL database.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{PATCH0}

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
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension/anon
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/data/*.csv %{buildroot}%{pginstdir}/share/extension/anon/
cp -a %{_builddir}/%{srcdir}/data/en_US/fake/*.csv %{buildroot}%{pginstdir}/share/extension/anon/
cp -a %{_builddir}/%{srcdir}/data/en_US %{buildroot}%{pginstdir}/share/extension/anon/
cp -a %{_builddir}/%{srcdir}/data/fr_FR %{buildroot}%{pginstdir}/share/extension/anon/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/extension/anon
%doc README.md AUTHORS.md
%license LICENSE.md
%exclude /usr/lib/.build-id

%changelog
* Sat Jul 18 2026 Vonng <rh@vonng.com> - 3.1.3-2PIGSTY
- Restore the flattened en_US fake-data CSV layout required by anon.init()

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 3.1.3-1PIGSTY
- Update to upstream 3.1.3 and migrate the locked dependency graph to pgrx 0.19.1

* Sun Jun 14 2026 Vonng <rh@vonng.com> - 3.1.1-1PIGSTY
- Upgrade to upstream 3.1.1
- Patch Cargo dependencies to build with cargo-pgrx 0.18.1

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
