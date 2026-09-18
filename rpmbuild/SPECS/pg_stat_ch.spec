%global _build_id_links none
%global pname pg_stat_ch
%global sname pg_stat_ch
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global vcpkg_commit cd61e1e26a038e82d6550a3ebbe0fbbfe7da78e3

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_stat_ch only supports PostgreSQL 16 through 18}
%endif

%if 0%{?rhel} && 0%{?rhel} < 9
%{error:pg_stat_ch 0.4.0 requires EL9 or later}
%endif

%ifarch aarch64
%global vcpkg_triplet arm64-linux-pic
%global vcpkg_host_triplet arm64-linux-release
%else
%global vcpkg_triplet x64-linux-pic
%global vcpkg_host_triplet x64-linux-release
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.4.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL query telemetry exporter to ClickHouse
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT AND OpenSSL
URL:            https://github.com/ClickHouse/pg_stat_ch
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pg_stat_ch-0.4.0.patch
# Normalized from https://api.pgxn.org/dist/pg_stat_ch/0.4.0/pg_stat_ch-0.4.0.zip

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  bison cmake flex gcc gcc-c++ git make ninja-build openssl-devel
BuildRequires:  curl zip unzip tar pkgconf-pkg-config perl-core python3
Requires:       postgresql%{pgmajorversion}-server

%description
pg_stat_ch captures per-query telemetry from PostgreSQL and exports raw events to
ClickHouse in real time. This package builds the upstream-pinned vcpkg Arrow and
OpenTelemetry dependency stack for PostgreSQL %{pgmajorversion}.

%prep
%autosetup -p1 -n %{srcdir}

%build
%set_build_flags
VCPKG_ROOT="$HOME/.cache/pg_stat_ch/vcpkg-%{vcpkg_commit}"
VCPKG_BINARY_CACHE="$HOME/.cache/pg_stat_ch/vcpkg-archives"
if [ ! -d "$VCPKG_ROOT/.git" ]; then
    mkdir -p "$(dirname "$VCPKG_ROOT")"
    git init -q "$VCPKG_ROOT"
    git -C "$VCPKG_ROOT" remote add origin https://github.com/microsoft/vcpkg.git
    git -C "$VCPKG_ROOT" fetch --depth=1 origin "%{vcpkg_commit}"
    git -C "$VCPKG_ROOT" checkout -q --detach FETCH_HEAD
fi
test "$(git -C "$VCPKG_ROOT" rev-parse HEAD)" = "%{vcpkg_commit}"
if [ ! -x "$VCPKG_ROOT/vcpkg" ]; then
    (cd "$VCPKG_ROOT" && ./bootstrap-vcpkg.sh -disableMetrics)
fi
mkdir -p "$VCPKG_BINARY_CACHE"
export VCPKG_MAX_CONCURRENCY="${VCPKG_MAX_CONCURRENCY:-2}"

VCPKG_ROOT="$VCPKG_ROOT" \
VCPKG_DISABLE_METRICS=1 \
VCPKG_DEFAULT_BINARY_CACHE="$VCPKG_BINARY_CACHE" \
cmake -S . -B build -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE="$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake" \
  -DVCPKG_TARGET_TRIPLET=%{vcpkg_triplet} \
  -DVCPKG_HOST_TRIPLET=%{vcpkg_host_triplet} \
  -DVCPKG_OVERLAY_TRIPLETS="$PWD/triplets" \
  -DPG_STAT_CH_PACKAGE_VERSION=%{version} \
  -DPG_CONFIG=%{pginstdir}/bin/pg_config \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel 2

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build

%check
test -f build/%{pname}.so
test -f %{buildroot}%{pginstdir}/share/extension/%{pname}.control
test -f %{buildroot}%{pginstdir}/share/extension/%{pname}--0.3--0.4.sql

%files
%doc README.md INSTALL.md docs/
%license LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.4.0-1PGSTY
- Update to upstream 0.4.0 with its pinned vcpkg Arrow and OpenTelemetry stack

* Sat Apr 18 2026 Vonng <rh@vonng.com> - 0.3.6-1PIGSTY
- Restrict RPM builds to EL9+ because EL8 builder repos do not ship the gRPC stack required by the packaged opentelemetry path

* Thu Apr 16 2026 Vonng <rh@vonng.com> - 0.3.6-1PIGSTY
- Update to upstream 0.3.6 using the normalized PGXN source tarball
- Keep EL9 builds on the packaged gRPC/abseil stack instead of the vendored FetchContent path

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.3.4-1PIGSTY
- Update to upstream 0.3.4 using the normalized pg_stat_ch-0.3.4.tar.gz source tarball
- Keep EL9 builds on system gRPC/abseil with the shared rpm/deb patch

* Wed Apr 08 2026 Vonng <rh@vonng.com> - 0.3.3-1PIGSTY
- https://github.com/ClickHouse/pg_stat_ch/releases/tag/v0.3.3
- Keep EL9 build on system gRPC/abseil with vendored sources
