%global debug_package %{nil}
%global pname pg_lake
%global sname pg_lake
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

Name:		%{sname}_%{pgmajorversion}
Version:	3.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension that integrates Iceberg and data lake files
License:	Apache-2.0
URL:		https://github.com/Snowflake-Labs/pg_lake
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/Snowflake-Labs/pg_lake/archive/refs/tags/v3.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cmake >= 3.4
BuildRequires:	ninja-build
BuildRequires:	gcc-c++
BuildRequires:	openssl-devel
BuildRequires:	libcurl-devel
BuildRequires:	perl libtool which patch

# RHEL/CentOS 8+ specific build dependencies
%if 0%{?rhel} >= 8
BuildRequires:	readline-devel
BuildRequires:	zlib-devel flex bison
BuildRequires:	libxml2-devel libxslt-devel
BuildRequires:	libicu-devel
BuildRequires:	geos-devel proj-devel gdal-devel
BuildRequires:	json-c-devel protobuf-c-devel
BuildRequires:	uuid-devel
BuildRequires:	lz4-devel xz-devel snappy-devel
BuildRequires:	perl-IPC-Run perl-IPC-Cmd
BuildRequires:	jansson-devel jq
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	libcurl openssl

%description
pg_lake integrates Iceberg and data lake files into PostgreSQL, allowing you to
use Postgres as a stand-alone lakehouse system that supports transactions and
fast queries on Iceberg tables. It provides native support for Apache Iceberg
format, enabling efficient analytical queries on large-scale data directly
from PostgreSQL.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

# Install vcpkg for dependency management
export VCPKG_VERSION=2025.01.13
export VCPKG_ROOT=%{_builddir}/vcpkg
if [ ! -d "$VCPKG_ROOT" ]; then
    git clone https://github.com/Microsoft/vcpkg.git $VCPKG_ROOT
    cd $VCPKG_ROOT
    git checkout %{VCPKG_VERSION}
    ./bootstrap-vcpkg.sh
    cd -
fi

%build
export PATH=%{pginstdir}/bin:$PATH
export VCPKG_ROOT=%{_builddir}/vcpkg
export PATH=$VCPKG_ROOT:$PATH

# Configure build environment
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
export CFLAGS
export CXXFLAGS

# Build pg_lake modules
mkdir -p build
cd build

# Configure with cmake
cmake .. \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{pginstdir} \
    -DPG_CONFIG=%{pginstdir}/bin/pg_config \
    -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake

# Build the extension
ninja %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin:$PATH

cd build
DESTDIR=%{buildroot} ninja install

# Install additional components if present
cd ..
if [ -d pg_lake_iceberg ]; then
    cd pg_lake_iceberg
    %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}
    cd ..
fi

if [ -d pg_lake_table ]; then
    cd pg_lake_table
    %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}
    cd ..
fi

if [ -d pg_map ]; then
    cd pg_map
    %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}
    cd ..
fi

%post
# Inform the user about loading the extension
if [ $1 -eq 1 ]; then
    echo "pg_lake extension has been installed."
    echo "To use it, connect to your PostgreSQL database and run:"
    echo "  CREATE EXTENSION pg_lake;"
    echo "  CREATE EXTENSION pg_lake_iceberg;"
    echo "  CREATE EXTENSION pg_lake_table;"
    echo "  CREATE EXTENSION pg_map;"
fi

%files
%defattr(-, root, root)
%doc README.md
%license LICENSE
%{pginstdir}/lib/pg_lake*.so
%{pginstdir}/lib/pg_map*.so
%{pginstdir}/share/extension/pg_lake*.control
%{pginstdir}/share/extension/pg_lake*.sql
%{pginstdir}/share/extension/pg_map*.control
%{pginstdir}/share/extension/pg_map*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{pname}*
   %{pginstdir}/lib/bitcode/pg_lake_iceberg*
   %{pginstdir}/lib/bitcode/pg_lake_table*
   %{pginstdir}/lib/bitcode/pg_map*
%endif

%changelog
* Tue Nov 05 2025 Vonng <rh@vonng.com> - 3.0-1PIGSTY
- Initial RPM release for pg_lake v3.0
- PostgreSQL extension for Iceberg and data lake integration
- Used by PGSTY/PIGSTY <https://pgsty.com>