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

BuildRequires:	cmake gcc-c++ ninja-build openssl-devel pkgconf-pkg-config
BuildRequires:	protobuf-devel protobuf-compiler grpc-devel grpc-plugins abseil-cpp-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_stat_ch captures per-query telemetry from PostgreSQL and exports raw events to
ClickHouse in real time.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{_specdir}/patches/pg_stat_ch-0.3.4-use-system-grpc-absl-and-std-unordered-map.patch

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
- Keep EL9 builds on system gRPC/abseil with the shared rpm/deb patch

* Wed Apr 08 2026 Vonng <rh@vonng.com> - 0.3.3-1PIGSTY
- https://github.com/ClickHouse/pg_stat_ch/releases/tag/v0.3.3
- Keep EL9 build on system gRPC/abseil with vendored sources

* Mon Apr 06 2026 Vonng <rh@vonng.com> - 0.3.2-1PIGSTY
- Restrict builds to PostgreSQL 16+ after EL10A validation

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.3.2-1PIGSTY
- Initial RPM release, using system gRPC/abseil on EL9 to avoid network fetches
