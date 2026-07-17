%define debug_package %{nil}
%global pname vectorscale
%global sname pgvectorscale
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgvectorscale only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.9.0
Release:	3PIGSTY%{?dist}
Summary:	A complement to pgvector for high performance, cost efficient vector search on large workloads.
License:	PostgreSQL
URL:		https://github.com/timescale/pgvectorscale
Source0:    pgvectorscale-%{version}.tar.gz
Patch0:     pgvectorscale-0.9.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server pgvector_%{pgmajorversion} >= 0.7.0

%description
pgvectorscale builds on pgvector with higher performance embedding search and cost-efficient storage for AI applications.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{PATCH0}

%build
cd %{_builddir}/%{sname}-%{version}/pgvectorscale
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.1
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_EXPECTED=338893d63d5651d59494fae6f0068a854e06cb30a844a1411f8c4f4157820975
LOCK_BEFORE=$(sha256sum ../Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_EXPECTED" ]; then
	echo "unexpected Cargo.lock checksum: $LOCK_BEFORE" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
%ifarch x86_64
export RUSTFLAGS="${RUSTFLAGS:-} -C target-feature=+avx2,+fma -C link-arg=-Wl,--no-gc-sections"
%else
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
%endif
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion},build_parallel --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum ../Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}-%{version}.so       %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.9.0-3PIGSTY
- Build with cargo-pgrx 0.19.1 and a locked dependency graph
- Keep AVX2/FMA optimization on x86_64 while allowing native aarch64 builds
- Preserve the parallel index-build feature and linker metadata retention flag

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.9.0-2PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Mon Nov 17 2025 Vonng <rh@vonng.com> - 0.9.0-1PIGSTY
- add pg18 support, drop pg13 support
* Fri Oct 31 2025 Vonng <rh@vonng.com> - 0.8.0-2PIGSTY
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 0.8.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.7.1-1PIGSTY
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.6.0-1PIGSTY
- https://github.com/timescale/pgvectorscale/releases/tag/0.6.0
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.5.1-1PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.4.0-1PIGSTY
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
