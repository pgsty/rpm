%define debug_package %{nil}
%global pname pgcontext
%global sname pgcontext
%global srcdir pgContext-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pgcontext only supports PostgreSQL 17 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PGSTY%{?dist}
Summary:	Hybrid vector and full-text retrieval engine for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/evokoa/pgcontext
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgContext/0.2.0/pgContext-0.2.0.zip
Patch0:		pgcontext-0.2.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server
Recommends:	pgvector_%{pgmajorversion}

%description
pgcontext provides dense vector search, metadata-filtered approximate search,
and hybrid dense plus full-text retrieval inside PostgreSQL. It also ships an
optional pgcontext_pgvector compatibility bridge.

%prep
%autosetup -p1 -n %{srcdir}

%build
cd %{_builddir}/%{srcdir}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
export RUSTUP_TOOLCHAIN=stable

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
grep -Fq 'pgrx = "=0.19.1"' Cargo.toml
grep -Fq 'pgrx-tests = "=0.19.1"' Cargo.toml
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked
LOCK_SHA256=$(sha256sum Cargo.lock | awk '{print $1}')
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v -p context-pg --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_SHA256" = "$(sha256sum Cargo.lock | awk '{print $1}')" || {
	echo "Cargo.lock changed during package" >&2
	exit 1
}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}
PKGDIR=%{_builddir}/%{srcdir}/target/release/%{pname}-pg%{pgmajorversion}
test -d "$PKGDIR%{pginstdir}"
cp -a "$PKGDIR%{pginstdir}/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGDIR%{pginstdir}/share/extension/%{pname}"*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 sql/%{pname}--0.1.0--0.2.0.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{pname}_pgvector.control %{buildroot}%{pginstdir}/share/extension/
install -m 644 sql/%{pname}_pgvector--0.2.0.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/
install -m 644 NOTICE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/NOTICE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}_pgvector.control
%{pginstdir}/share/extension/%{pname}_pgvector--*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 27 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Add RPM package for PostgreSQL 17 and 18
- Build the upstream locked workspace with cargo-pgrx 0.19.1
- Preserve the upstream Apache NOTICE in the package payload
