%define debug_package %{nil}
%global pname pg_command_fw
%global sname pg_command_fw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_command_fw only supports PostgreSQL 15 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	3PIGSTY%{?dist}
Summary:	DDL and utility command firewall for PostgreSQL
License:	BSD-3-Clause
URL:		https://github.com/rustwizard/pg_command_fw
Source0:	%{sname}-%{version}.tar.gz
#           normalized source tarball from the upstream PGXN release archive

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pg_command_fw is a PostgreSQL extension that intercepts and blocks selected
DDL, utility commands, and dangerous built-in functions through configurable
hooks.

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
mkdir -p %{_builddir}/%{sname}-%{version}
tar -C %{_builddir}/%{sname}-%{version} --strip-components=1 -xzf %{SOURCE0}
patch -d %{_builddir}/%{sname}-%{version} -p1 --forward -f < %{_specdir}/patches/pg-command-fw-0.1.0.patch

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{sname}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{sname}-%{version}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.1.0-3PIGSTY
- Migrate the direct-on-pristine source patch and locked dependency graph to pgrx 0.19.1
- Add the previously absent Cargo.lock and verify cargo pgrx package does not rewrite it

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.1.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Mon Apr 06 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Restrict builds to PostgreSQL 15+ and initialize cargo-pgrx with the active pgmajorversion

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
