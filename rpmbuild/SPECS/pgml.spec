%global pname pgml
%global sname pgml
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global pgrx_version 0.12.9
%global rust_version 1.84.0

Name:		%{pname}_%{pgmajorversion}
Version:	2.10.0
Release:	1PGSTY%{?dist}
Summary:	PostgresML is a complete MLOps platform in a PostgreSQL extension. Build simpler, faster and more scalable models right inside your database.
License:	MIT
URL:		https://github.com/postgresml/postgresml
Source0:    pgml-%{version}.tar.gz
Patch0:     pgml-2.10.0-build-id-sha1.patch
Patch1:     pgml-2.10.0-lightgbm-cstdint.patch
Patch2:     pgml-2.10.0-cold-cache.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang-devel openblas-devel
%if 0%{?rhel} >= 10
BuildRequires:	python3-devel
%else
BuildRequires:	python3.11-devel
%endif
Requires:	postgresql%{pgmajorversion}-server

%description
PostgresML is a machine learning extension for PostgreSQL that enables you to perform training and inference on text and tabular data using SQL queries.
 With PostgresML, you can seamlessly integrate machine learning models into your PostgreSQL database and harness the power of cutting-edge algorithms to process data efficiently.

%prep
%setup -q -n %{pname}-%{version}
%patch -P 0 -p1
%patch -P 2 -p1

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
export PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH
%if 0%{?rhel} >= 10
export PYO3_PYTHON=/usr/bin/python3.12
%else
export PYO3_PYTHON=/usr/bin/python3.11
%endif

CURRENT_RUST=$(rustc --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_RUST" != "%{rust_version}" ]; then
	echo "Rust %{rust_version} is required, found ${CURRENT_RUST:-missing}; run pig build rust %{rust_version} before building" >&2
	exit 1
fi

CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "%{pgrx_version}" ]; then
	echo "cargo-pgrx %{pgrx_version} is required, found ${CURRENT_PGRX:-missing}; run pig build pgrx -v %{pgrx_version} before building" >&2
	exit 1
fi

sha256sum Cargo.lock > .pgml-cargo-lock.before
cargo fetch --locked

LOCK_HASH=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_HASH" != "f976f1aecf1b66d562e9a0cafec4748aaa7602be8db24af93f8e02ca6c5fe5d8" ]; then
	echo "unexpected Cargo.lock sha256: $LOCK_HASH" >&2
	exit 1
fi
grep -Fq 'source = "git+https://github.com/postgresml/lightgbm-rs?branch=main#978dd69f6c7aafb8500ecb255f2248fde80ebc97"' Cargo.lock || {
	echo "locked lightgbm-rs revision mismatch" >&2
	exit 1
}
CARGO_HOME_DIR=${CARGO_HOME:-$HOME/.cargo}
set -- $(find "$CARGO_HOME_DIR/git/checkouts" -type f -path '*/978dd69*/lightgbm-sys/lightgbm/src/io/json11.cpp' -print)
if [ "$#" -ne 1 ]; then
	echo "expected one locked LightGBM json11.cpp, found $#" >&2
	exit 1
fi
JSON11=$1
CHECKOUT=$(cd "$(dirname "$JSON11")/../../../.." && pwd)
SUBMODULE="$CHECKOUT/lightgbm-sys/lightgbm"
if [ "$(git -c safe.directory="$CHECKOUT" -C "$CHECKOUT" rev-parse HEAD)" != "978dd69f6c7aafb8500ecb255f2248fde80ebc97" ]; then
	echo "lightgbm-rs checkout revision mismatch" >&2
	exit 1
fi
if [ "$(git -c safe.directory="$SUBMODULE" -C "$SUBMODULE" rev-parse HEAD)" != "dce7e58b020bc14b69eefc31546c366971ecb2d9" ]; then
	echo "LightGBM submodule revision mismatch" >&2
	exit 1
fi
JSON11_HASH=$(sha256sum "$JSON11" | awk '{print $1}')
case "$JSON11_HASH" in
	50721d4783935d481779f137c5459668c872ec02826193333d1ac1b2122770b2)
		patch --fuzz=0 --batch --forward -d "$CHECKOUT/lightgbm-sys" -p1 < %{PATCH1}
		;;
	326748d9e9b14ed90638bd95cff58435d51a5008ea350aa86796dca4d5cc5ba2)
		:
		;;
	*)
		echo "unexpected LightGBM json11.cpp sha256: $JSON11_HASH" >&2
		exit 1
		;;
esac
test "$(sha256sum "$JSON11" | awk '{print $1}')" = "326748d9e9b14ed90638bd95cff58435d51a5008ea350aa86796dca4d5cc5ba2"

CARGO_NET_OFFLINE=true cargo pgrx package -v
sha256sum Cargo.lock > .pgml-cargo-lock.after
cmp .pgml-cargo-lock.before .pgml-cargo-lock.after

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{pname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.10.0-1PGSTY
- Build the checked-in Cargo.lock without cargo update using Rust 1.84.0 and pgrx 0.12.9
- Bind pyo3 to Python 3.11 on EL8/EL9 and Python 3.12 on EL10
- Use a SHA1 GNU build ID that RPM and Debian debug tooling can split
- Backport LightGBM's GCC 15 cstdint include fix with locked source guards
- Fix cold-cache project mapping and model hyperparameter restoration

* Tue Jan 21 2025 Vonng <rh@vonng.com> - 2.10.0
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 2.9.3
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 2.9.2
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 2.9.1
- Bump version to v2.9.1 with pgrx 0.11.3
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 2.8.1
- Bump version to v2.8.2 with PG 16 support
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 2.7.9
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
