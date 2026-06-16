%define debug_package %{nil}
%global pname pg_parquet
%global sname pg_parquet
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_parquet only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.5.1
Release:	2PIGSTY%{?dist}
Summary:	Copy to/from Parquet in S3 from within PostgreSQL
License:	PostgreSQL
URL:		https://github.com/CrunchyData/pg_parquet
Source0:	pg_parquet-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
pg_parquet is a PostgreSQL extension that allows you to read and write Parquet files, which are located in S3 or file system,
 from PostgreSQL via COPY TO/FROM commands. It depends on Apache Arrow project to read and write Parquet files and pgrx project to extend PostgreSQL's COPY command.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg-parquet-0.5.1.patch

%build
%if 0%{?rhel} >= 10
export CFLAGS=$(echo "${CFLAGS:-}" | sed -e 's/-flto=auto//g' -e 's/-flto[^ ]*//g' -e 's/-ffat-lto-objects//g')
export CXXFLAGS=$(echo "${CXXFLAGS:-}" | sed -e 's/-flto=auto//g' -e 's/-flto[^ ]*//g' -e 's/-ffat-lto-objects//g')
export LDFLAGS=$(echo "${LDFLAGS:-}" | sed -e 's/-flto=auto//g' -e 's/-flto[^ ]*//g')
%endif
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.18.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo update -p pgrx --precise $PGRX_VERSION
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo update -p pgrx-tests --precise $PGRX_VERSION
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

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
%license LICENSE
%exclude /usr/lib/.build-id

%changelog
* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.5.1-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.5.1-1PIGSTY
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 0.4.3-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.4.0-1PIGSTY
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.3.1-1PIGSTY
* Wed Jan 08 2025 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.1.1-1PIGSTY
* Sat Oct 19 2024 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>