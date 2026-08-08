%define debug_package %{nil}
%global pname pg_mentat
%global sname pg_mentat
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_mentat supports PostgreSQL 14 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.5.7
Release:        1PIGSTY%{?dist}
Summary:        Datomic-compatible Datalog query engine for PostgreSQL
License:        Apache-2.0
URL:            https://github.com/gburd/pg_mentat
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/gburd/pg_mentat/archive/refs/tags/v1.5.7.tar.gz
Patch0:         pg-mentat-1.5.7-pgrx-0.19.1.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cargo clang rust rustfmt
Requires:       postgresql%{pgmajorversion}-server

%description
pg_mentat implements a Datomic-compatible immutable fact store and Datalog
query engine inside PostgreSQL, including pull queries, time travel, and
transaction processing through SQL functions.

%prep
%autosetup -p1 -n %{srcdir}

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
grep -Fq 'pgrx = "=0.19.1"' pg_mentat/Cargo.toml
grep -Fq 'pgrx-tests = "=0.19.1"' pg_mentat/Cargo.toml
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true \
    cargo pgrx package -v -p %{pname} --no-default-features \
    --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_SHA256" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
PKGDIR=%{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}
test -d "$PKGDIR%{pginstdir}"
install -m 644 pg_mentat/sql/%{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGDIR%{pginstdir}/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}"*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Aug 07 2026 Vonng <rh@vonng.com> - 1.5.7-1PIGSTY
- Initial RPM release for pg_mentat 1.5.7 and PostgreSQL 14 through 18
- Migrate the locked dependency graph from upstream pgrx 0.17.0 to 0.19.1
