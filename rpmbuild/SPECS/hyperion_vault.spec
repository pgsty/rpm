%define debug_package %{nil}
%global pname hyperion_vault
%global sname hyperion_vault
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:hyperion_vault only supports PostgreSQL 18 in upstream metadata}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.0
Release:	1PIGSTY%{?dist}
Summary:	Encrypted secrets vault for PostgreSQL
License:	GPL-3.0-or-later
URL:		https://github.com/hyperiondb/hyperion-vault
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/hyperion_vault/0.3.0/hyperion_vault-0.3.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
hyperion_vault stores secrets encrypted at rest in PostgreSQL using a pgrx
extension and a vault schema. Its rotation supervisor is a background worker,
so production use requires loading hyperion_vault through
shared_preload_libraries.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}/extension
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.18.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run

# pgrx 0.18 embeds extension schema metadata in a linker section; without this
# flag the EL9A linker can garbage-collect it and cargo-pgrx reports a missing
# .pgrxsc section during packaging.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name} %{buildroot}%{_licensedir}/%{name}

PKGROOT="$(find %{_builddir}/%{sname}-%{version} -path "*/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}" -type d | head -n 1)"
test -n "$PKGROOT"
cp -a "$PKGROOT/lib/%{pname}.so" %{buildroot}%{pginstdir}/lib/
cp -a "$PKGROOT/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PKGROOT/share/extension/%{pname}"*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{sname}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{sname}-%{version}/LICENCE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENCE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id
%exclude /usr/lib/.build-id/*
%exclude /usr/lib/.build-id/*/*

%changelog
* Sun Jun 14 2026 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.3.0
- Build PostgreSQL 18 pgrx extension with cargo-pgrx 0.18.1
