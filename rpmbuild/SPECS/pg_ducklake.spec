%global pname pg_ducklake
%global sname pg_ducklake
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif
# PGXS in the current EL9 builder points LLVM_BINPATH at llvm20 while the image
# ships llvm21, so ship the primary extension package without bitcode for now.
%global llvm 0

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	DuckLake lakehouse extension for PostgreSQL
License:	MIT
URL:		https://github.com/relytcloud/pg_ducklake
# Source0 is a repacked v1.0.0 release tarball with submodules:
# duckdb 9a64d338f2fa1d3c1d43c016b09c538b529dd397
# pg_ducklake/third_party/ducklake 93cc490d9b5554f6fd5322dbef23f41d4fa91bb8
# pg_ducklake/third_party/duckdb-postgres c89234f0b1985f4ee0f52f16e742a1ab2d4ae4f0
# pg_ducklake/third_party/duckdb-postgres/database-connector 746b56c4063f3682f4eb4facdc49408ed1885555
# pg_ducklake/third_party/duckdb-postgres/postgres REL_15_13
Source0:	%{sname}-%{version}.tar.gz
Source1:	CRoaring-4.7.1-amalgamation.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc gcc-c++ make cmake ninja-build patch pkgconf-pkg-config
BuildRequires:	bison flex zlib-devel readline-devel libxml2-devel libxslt-devel
BuildRequires:	openssl-devel libcurl-devel lz4-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_ducklake is a PostgreSQL extension for managed DuckLake tables, backed by
DuckDB and Parquet files. It requires shared_preload_libraries = 'pg_ducklake'
before CREATE EXTENSION.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}-rpm-tarball-build.patch
tar -xzf %{SOURCE1}
mkdir -p .rpm-licenses
cp LICENSE .rpm-licenses/%{sname}-LICENSE
cp CRoaring-4.7.1/LICENSE .rpm-licenses/CRoaring-LICENSE
cp pg_ducklake/third_party/duckdb-postgres/LICENSE .rpm-licenses/duckdb-postgres-LICENSE
cp pg_ducklake/third_party/duckdb-postgres/database-connector/LICENSE .rpm-licenses/database-connector-LICENSE
cp pg_ducklake/third_party/duckdb-postgres/postgres/COPYRIGHT .rpm-licenses/postgresql-COPYRIGHT

%build
croaring_prefix="$(pwd)/.croaring"
croaring_src="$(pwd)/CRoaring-4.7.1"
mkdir -p "$croaring_prefix/include/roaring" "$croaring_prefix/lib/cmake/roaring" "$croaring_src/build"
cp -a "$croaring_src/include/roaring/." "$croaring_prefix/include/roaring/"
cp -a "$croaring_src/cpp/roaring/." "$croaring_prefix/include/roaring/"
for src in $(find "$croaring_src/src" -name '*.c' | sort); do
	obj="$(echo "${src#$croaring_src/}" | tr '/.' '__').o"
	%{__cc} %{optflags} -fPIC -I"$croaring_src/include" -c "$src" -o "$croaring_src/build/$obj"
done
ar cr "$croaring_prefix/lib/libroaring.a" "$croaring_src"/build/*.o
cat > "$croaring_prefix/lib/cmake/roaring/roaringConfig.cmake" <<'EOF'
get_filename_component(_roaring_prefix "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)
add_library(roaring::roaring STATIC IMPORTED)
set_target_properties(roaring::roaring PROPERTIES
  IMPORTED_LOCATION "${_roaring_prefix}/lib/libroaring.a"
  INTERFACE_INCLUDE_DIRECTORIES "${_roaring_prefix}/include")
add_library(roaring::roaring-headers INTERFACE IMPORTED)
set_target_properties(roaring::roaring-headers PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "${_roaring_prefix}/include")
add_library(roaring::roaring-headers-cpp INTERFACE IMPORTED)
set_target_properties(roaring::roaring-headers-cpp PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "${_roaring_prefix}/include")
EOF
cp "$croaring_prefix/lib/cmake/roaring/roaringConfig.cmake" "$croaring_prefix/lib/cmake/roaring/roaring-config.cmake"

CMAKE_PREFIX_PATH="$croaring_prefix" PATH=%{pginstdir}/bin:$PATH PG_CONFIG=%{pginstdir}/bin/pg_config \
	%{__make} ROARING_LIB_DIR="$croaring_prefix/lib" with_llvm=no -j2

%install
%{__rm} -rf %{buildroot}
CMAKE_PREFIX_PATH="$(pwd)/.croaring" PATH=%{pginstdir}/bin:$PATH PG_CONFIG=%{pginstdir}/bin/pg_config \
	%{__make} ROARING_LIB_DIR="$(pwd)/.croaring/lib" with_llvm=no -j2 install DESTDIR=%{buildroot}

%files
%doc README.md pg_ducklake/docs
%license .rpm-licenses/*
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%exclude %{pginstdir}/lib/bitcode/*
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for pg_ducklake 1.0.0
