%global sname h3-pg
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:h3-pg supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        4.5.0
Release:        1PGSTY%{?dist}
Summary:        H3 hierarchical geospatial indexing for PostgreSQL
License:        Apache-2.0
URL:            https://github.com/postgis/h3-pg
Source0:        %{sname}-%{version}.tar.gz
Source1:        h3-4.5.0.tar.gz
# The H3 core archive matches the SHA256 pinned by upstream h3-pg 4.5.0.
BuildRequires:  gcc, cmake >= 3.20, make
BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:  llvm-devel >= 19.0, clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
H3 and h3_postgis provide PostgreSQL bindings for the H3 hierarchical
geospatial indexing library. The released H3 core is linked statically.

%prep
%setup -q -n %{sname}-%{version}
mkdir -p vendor/h3
echo '0da8a392a6ff77e76b60e6a331a49497d0935b6b7b6899da7a3e2786139b0441  %{SOURCE1}' | sha256sum -c -
tar --strip-components=1 -xf %{SOURCE1} -C vendor/h3
cp vendor/h3/LICENSE H3-LICENSE
%if !%llvm
# The upstream CMake helper otherwise follows PostgreSQL's LLVM configuration.
sed -i 's/if(NOT PostgreSQL_WITH_LLVM)/if(TRUE)/' cmake/AddPostgreSQLExtension.cmake
%endif

%build
%set_build_flags
cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_TESTING=OFF -DBUILD_SHARED_LIBS=OFF \
    -DFETCHCONTENT_SOURCE_DIR_H3="$PWD/vendor/h3" \
    -DPostgreSQL_CONFIG=%{pginstdir}/bin/pg_config
cmake --build build --parallel %{_smp_build_ncpus}

%install
# Install the extension component without exporting the vendored static core.
DESTDIR=%{buildroot} cmake --install build --component h3-pg

%files
%license LICENSE H3-LICENSE
%doc README.md
%{pginstdir}/lib/h3.so
%{pginstdir}/lib/h3_postgis.so
%{pginstdir}/share/extension/h3*.sql
%{pginstdir}/share/extension/h3*.control
%if %llvm
%{pginstdir}/lib/bitcode/h3*
%endif

%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 4.5.0-1PGSTY
- Update h3-pg and its pinned H3 core to 4.5.0.
- Preserve debug symbols and package LLVM bitcode with the main extension.

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 4.2.3-1PIGSTY
- Rebuild EL8 x86_64 packages for PostgreSQL 17 and 18

* Tue Jun 24 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.3-1PGDG
- Update to 4.2.3
