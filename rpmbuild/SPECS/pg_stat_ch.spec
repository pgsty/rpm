%global pname pg_stat_ch
%global sname pg_stat_ch
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16
%{error:pg_stat_ch only supports PostgreSQL 16+}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.4
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL query telemetry exporter to ClickHouse
License:	Apache-2.0
URL:		https://github.com/ClickHouse/pg_stat_ch
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	cmake gcc-c++ ninja-build openssl-devel pkgconf-pkg-config python3
BuildRequires:	protobuf-devel protobuf-compiler grpc-devel grpc-plugins abseil-cpp-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_stat_ch captures per-query telemetry from PostgreSQL and exports raw events to
ClickHouse in real time.

%prep
%setup -q -n %{srcdir}

python3 - <<'PY'
from pathlib import Path


def rewrite(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"pattern not found in {path}")
    p.write_text(text.replace(old, new, 1))


rewrite(
    "CMakeLists.txt",
    """# Always use vendored gRPC + abseil (never pick up system packages).
# This prevents find_package(gRPC) from short-circuiting FetchContent
# and leaving absl:: targets undefined.
set(CMAKE_DISABLE_FIND_PACKAGE_gRPC TRUE)
add_subdirectory(third_party/opentelemetry-cpp EXCLUDE_FROM_ALL)
""",
    """# Always use vendored gRPC + abseil (never pick up system packages).
add_subdirectory(third_party/opentelemetry-cpp EXCLUDE_FROM_ALL)
# EL9 builds prefer the packaged Abseil configuration.
find_package(absl CONFIG REQUIRED)
""",
)

rewrite(
    "src/export/otel_exporter.cc",
    "#include <absl/container/flat_hash_map.h>",
    "#include <unordered_map>",
)
rewrite(
    "src/export/otel_exporter.cc",
    "const absl::flat_hash_map<string, string>& base,",
    "const std::unordered_map<string, string>& base,",
)
rewrite(
    "src/export/otel_exporter.cc",
    "const absl::flat_hash_map<string, string>& base_;",
    "const std::unordered_map<string, string>& base_;",
)
rewrite(
    "src/export/otel_exporter.cc",
    "absl::flat_hash_map<string, string> current_row_tags;",
    "std::unordered_map<string, string> current_row_tags;",
)

rewrite(
    "src/hooks/query_normalize_state.cc",
    """#include <cstring>
#include <string_view>

#include "absl/hash/hash.h"
""",
    """#include <cstring>
#include <functional>
#include <string_view>
""",
)
rewrite(
    "src/hooks/query_normalize_state.cc",
    """struct PschStatementKeyHash {
  size_t operator()(const PschStatementKey& key) const {
    return absl::HashOf(
        std::string_view(key.source_text != nullptr ? key.source_text : "", key.source_text_len),
        key.stmt_location, key.stmt_len);
  }
};
""",
    """struct PschStatementKeyHash {
  static size_t HashCombine(size_t seed, size_t value) {
    return seed ^ (value + 0x9e3779b97f4a7c15ULL + (seed << 6) + (seed >> 2));
  }

  size_t operator()(const PschStatementKey& key) const {
    size_t seed = std::hash<std::string_view>{}(
        std::string_view(key.source_text != nullptr ? key.source_text : "", key.source_text_len));
    seed = HashCombine(seed, std::hash<int>{}(key.stmt_location));
    seed = HashCombine(seed, std::hash<int>{}(key.stmt_len));
    return seed;
  }
};
""",
)
PY

%build
git config --global http.version HTTP/1.1
cmake -B build -G Ninja \
  -DPG_CONFIG=%{pginstdir}/bin/pg_config \
  -DOTELCPP_PROTO_PATH=%{_builddir}/%{srcdir}/third_party/opentelemetry-cpp/third_party/opentelemetry-proto \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel 2

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build

%files
%doc README.md
%license LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.3.4-1PIGSTY
- Update to upstream 0.3.4 using the normalized pg_stat_ch-0.3.4.tar.gz source tarball
- Keep EL9 builds on system gRPC/abseil with the standard-library hashing patch

* Wed Apr 08 2026 Vonng <rh@vonng.com> - 0.3.3-1PIGSTY
- https://github.com/ClickHouse/pg_stat_ch/releases/tag/v0.3.3
- Keep EL9 build on system gRPC/abseil with vendored sources

* Mon Apr 06 2026 Vonng <rh@vonng.com> - 0.3.2-1PIGSTY
- Restrict builds to PostgreSQL 16+ after EL10A validation

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.3.2-1PIGSTY
- Initial RPM release, using system gRPC/abseil on EL9 to avoid network fetches
