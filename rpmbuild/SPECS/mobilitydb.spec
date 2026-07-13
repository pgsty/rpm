%global sname mobilitydb
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:mobilitydb only supports PostgreSQL 14 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.3.0
Release:        1PIGSTY%{?dist}
Summary:        Geospatial trajectory data management and analysis platform
# MobilityDB is PostgreSQL-licensed; the shared library embeds GPL-2.0-or-later
# PostGIS liblwgeom/libpgcommon objects, as documented by debian/copyright.
License:        PostgreSQL AND GPL-2.0-or-later
URL:            https://mobilitydb.com/
Source0:        %{sname}-%{version}.tar.gz
# https://apt.postgresql.org/pub/repos/apt/pool/main/m/mobilitydb/mobilitydb_1.3.0.orig.tar.gz

# PGDG/Debian mobilitydb 1.3.0-2 patches, combined in their original order.
Patch0:         mobilitydb-1.3.0.patch

# Debian limits builds to 64-bit little-endian architectures. These are the two
# such architectures in the PGSTY RPM matrix.
ExclusiveArch:  x86_64 aarch64

BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgis36_%{pgmajorversion}
BuildRequires:  cmake >= 3.12
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  geos314-devel
BuildRequires:  proj96-devel
BuildRequires:  json-c-devel
BuildRequires:  gsl-devel

Requires:       postgresql%{pgmajorversion}-server
Requires:       postgis36_%{pgmajorversion}

%description
MobilityDB is a database management system for moving-object geospatial
trajectories. It extends PostgreSQL and PostGIS with temporal and
spatiotemporal types, indexes, and functions. This package also includes the
mobilitydb_datagen companion extension.

%prep
%autosetup -p1 -n MobilityDB-%{version}

%build
export PATH=%{pginstdir}/bin:$PATH
# Release mode supplies -DNDEBUG, matching Debian's maintainer CPPFLAGS.
# Use the same GEOS/PROJ ABI generation as the packaged PostGIS 3.6 build.
cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DPOSTGRESQL_PG_CONFIG=%{pginstdir}/bin/pg_config \
    -DGEOS_CONFIG=/usr/geos314/bin/geos-config \
    -DGEOS_INCLUDE_DIR=/usr/geos314/include \
    -DGEOS_LIBRARY=/usr/geos314/lib64/libgeos_c.so \
    -DPROJ_INCLUDE_DIRS=/usr/proj96/include \
    -DPROJ_LIBRARIES=/usr/proj96/lib64/libproj.so
cmake --build build -- %{?_smp_mflags}

# Upstream regression tests require a live PostgreSQL cluster. As in Debian,
# they are run against the installed package rather than inside the build root.

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build

%files
%license LICENSE.txt
%doc README.md
%{pginstdir}/lib/libMobilityDB-1.3.so
%{pginstdir}/share/extension/mobilitydb.control
%{pginstdir}/share/extension/mobilitydb--*.sql
%{pginstdir}/share/extension/mobilitydb_datagen.control
%{pginstdir}/share/extension/mobilitydb_datagen--*.sql

%changelog
* Sat Jul 11 2026 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
