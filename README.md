# PGSTY RPM Package Builder

Extension build scripts for PostgreSQL 15–19 on EL9/EL10.

- [Pigsty PGSQL Repo](https://pigsty.io/docs/repo/pgsql)
- [RPM Change Log](https://pigsty.io/docs/repo/pgsql/rpm)


## Current build scope

The active targets are PostgreSQL 15–19 and EL9/EL10 on x86_64/aarch64.
PG19 is enabled per extension after validation; the default target list does
not imply that every extension supports it. PG14 and EL8 are retired from
active orchestration. The [Rust/pgrx 0.20.0 pilot](doc/rust-pgrx-0.20.0-pilot.md)
records the lowest and highest PG versions tested per extension on Rocky Linux
9.9/aarch64 and Ubuntu 24.04/amd64. Heavy components and custom PostgreSQL
providers have separate build records.

The [2026-11-21 audit](doc/nonrust-pg19-20261121.md) and its
[machine-readable support matrix](doc/nonrust-pg19-20261121.json) record
upstream checks, actual PG ranges, pilot builds, runtime coverage and deferrals.
That audit used Rocky Linux 9.8/aarch64 and Ubuntu 24.04/amd64;
these results do not imply a production matrix or a repository publication.
Historical EL8 build records and Terraform templates remain archival references;
they are outside the active build matrix.

The [spec and patch review](doc/nonrust-spec-review-20261121.md) records
necessity, scope, validation limits and the per-extension commits.

## How to use?

You can build extension RPMs with [pig](https://pgext.cloud/pig).

```bash
curl https://repo.pigsty.cc/pig | bash -s 1.1.0
pig build repo
pig build tool
pig build spec # <--- get this repo, setup building environment
pig build rust
export PATH="$HOME/.cargo/bin:$PATH"
rustup toolchain install 1.100.0
export RUSTUP_TOOLCHAIN=1.100.0
pig build pgrx -v 0.20.0

# then build packages
pig build pkg timescaledb
pig build pkg pg_search
```

## Debug packages

Native builds keep compiler DWARF and generate the standard main,
`-debuginfo`, and `-debugsource` RPMs by default. Rust extensions remain
optimized release builds while setting Cargo's release debug level to `2` and
leaving stripping to RPM. Pure SQL/data/script packages with a genuine
`BuildArch: noarch` payload do not generate empty debug packages. Specs that
invoke CMake, Meson, Autoconf, or compilers directly must import RPM build flags
so the automatic split has real DWARF to package.

## PostGIS and the PGDG GIS stack

`rpmbuild/SPECS/postgis.spec` retains the PostGIS 3.7.0 fallback recipe for PostgreSQL 15–18 on
EL9/EL10 with `postgis37_<major>` package names. Raster, SFCGAL, topology,
client tools, GUI, utilities, and PDF documentation are retained. LLVM bitcode belongs to the
main package. Native payloads retain debuginfo and debugsource packages;
the empty upstream `devel` package is omitted. GDAL's Python tools and
Javadoc are `noarch`; its Java and Python native bindings retain debug
packages. The Javadoc patch fixes invalid links and makes generator errors
fail the build.

PostGIS 3.7 no longer ships `address_standardizer` or
`postgis_tiger_geocoder` in the core source tree. They are built independently
from their upstream archives as `address_standardizer_<major>` (3.7.0) and
`postgis_tiger_geocoder_<major>` (2025.2); the Tiger package is limited to
PostgreSQL 16–19 and is `noarch`.

PGDG already supplies PostGIS 3.7.0 for PG19 and the current GIS libraries on
the pilot platforms. Reuse those packages. For a required supplier gap, the
local fallback recipes have this dependency order:

1. `geos314` 3.14.1, `proj98` 9.8.1, and `sfcgal` 2.2.0.
2. `libgeotiff17` 1.7.4 and `librttopo` 1.1.0, then `libspatialite50` 5.1.0.
3. `gdal313` 3.13.3, including the PGDG Python 3.12 and Java bindings.
4. `postgis` 3.7.0 for the selected PostgreSQL major.
5. `address_standardizer` 3.7.0 and `postgis_tiger_geocoder` 2025.2 for the
   selected PostgreSQL major.

Build and install each library's runtime and development RPMs before
building its consumers. On EL9/EL10, system dependencies including CGAL,
Boost, and Arrow come from the builder's OS/EPEL repositories. The legacy
EL8 compatibility families are retired from active targets. Library targets
build once; `make postgis` selects the locally supported PostgreSQL 15–18
range, while `./build postgis 18` selects just PG18. The new GEOS/PROJ parallel
ABI families and SFCGAL 2.3.0 remain supplied by PGDG on the pilot platforms.

In a disposable pilot builder, exclude these GIS package families from
remote repositories after staging their build inputs, and install the
locally built RPMs explicitly. Otherwise `dnf builddep` can upgrade them
back to PGDG's higher release numbers before building the next component.
Keep all native debug packages and the normal RPM RPATH checks enabled.

[Source provenance](bin/postgis-sources.json) records the exact PGDG source
RPM URLs and SHA-256 hashes. The
[source manifest](rpmbuild/SPECS/manifests/postgis.sources.sha256) covers
the archives and auxiliary inputs stored in `src`. GDAL deliberately uses
PGDG's cleaned `gdal-3.13.3-fedora.tar.xz` and its provenance notice.

Inside a builder, first run `pig build get <package>`. If these new package
names are not yet available in the source catalog, copy only the missing
manifest-listed inputs into the builder's `~/rpmbuild/SOURCES/`. Verify the
manifest there, then run `./dep <package> 18` and `./build <package> 18`.
The local checkout's `rpmbuild/SOURCES/` must remain empty.

After installing the built RPMs, run `bin/postgis-test.sql` with `psql -f`
in a disposable database. It creates the four PostGIS 3.7.0 extensions and
checks GEOS overlay, PROJ transformation, SFCGAL 3D area, GDAL GeoTIFF
export/import, and topology creation. Run `bin/postgis-split-test.sql` in the
same database to check address parsing, US standardization, and, on PG16–19,
TIGER address normalization and loader SQL generation. A pilot on one builder does not
validate the other platforms or publish any package.

The PostGIS 3.6.4 full build on 2026-10-04 passed on `pgsty/el8{,a}:build`,
`pgsty/el9{,a}:build` and `pgsty/el10{,a}:build`: Rocky Linux 8.10, 9.8 and
10.2 on x86_64/aarch64, each with PostgreSQL 14–18. It produced 506 binary
RPMs (including 226 debug packages) and 76 SRPMs. PostGIS passed 21,300 SQL
regression executions across fresh installation and self-upgrade; RPM-side
CUnit tests were not separately run. Installed payloads, native dependencies,
GDAL Python/Java bindings, debug packages, LLVM bitcode and multi-version
coinstallation were verified. Artifacts and SHA-256 receipts are retained in
`yum/postgis-full-20261004/`; packages were collected locally, not published.

The 2026-11-05 EL8 gap build passed on Rocky Linux 8.10 with
`pgsty/el8:build` (x86_64) and `pgsty/el8a:build` (aarch64). PostGIS 3.7.0
and address_standardizer 3.7.0 cover PG14–18; TIGER 2025.2 covers PG16–18.
PGDG supplies the GIS dependencies: GEOS 3.14.1, PROJ 9.6.2, GDAL 3.8.5,
SFCGAL 1.5.2, and libgeotiff 1.7.4. EL8 explicitly supplies GMP flags because
its development package has no `gmp.pc`, and disables LTO through configure;
LLVM remains enabled. The standalone address parser no longer requires PostGIS.
Each platform directory contains 63 RPMs, including 30 debug packages. The
13 noarch RPMs are shared byte-for-byte, yielding 113 distinct RPMs and 23
SRPMs across both builders. Payloads, DWARF, main-package LLVM bitcode,
runtime dependencies, parallel PG installation, and both smoke scripts passed
for every supported target. RPMs and SHA-256 manifests are in
`yum/postgis37-el8-20261105/`; logs, source RPMs, build inputs, and QA receipts
are in `~/pgsty/artifacts/postgis37-el8-20261105/`. On the same day, 33 normal
RPMs per architecture entered `~/pgsty/repo/yum/pgsql/el8.{aarch64,x86_64}/`;
60 debug RPMs were archived separately under `~/pgsty/repo/pkg/debug/20261105/rpm/`.
Both repositories passed signing, metadata verification, and native EL8 client
downloads of all 66 package placements. The import report is
`~/pgsty/repo/reports/postgis37-el8-import-20261105.md`; CDN synchronization
has not been run.


## Babelfish (EL10A, PG17)

Current package chain:

1. `antlr4-runtime413` + `antlr4-runtime413-devel` (standalone ANTLR runtime)
2. `babelfish-17` (Babelfish PG 17.7 kernel + four core extensions)

Key files:

- `bin/babelfish.sh` (generate source tarball + ANTLR zip)
- `rpmbuild/SPECS/antlr4-runtime413.spec`
- `rpmbuild/SPECS/babelfish.spec`
- `rpmbuild/Makefile` target: `babelfish_all`

Generate sources:

```bash
bin/babelfish.sh
```

Build on EL10A (example):

```bash
cp ~/pgsty/rpm/src/babelfish-17-17.7-5.4.0.tar.gz ~/rpmbuild/SOURCES/
cp ~/pgsty/rpm/src/antlr4-cpp-runtime-4.13.2-source.zip ~/rpmbuild/SOURCES/
cp ~/pgsty/rpm/rpmbuild/SPECS/antlr4-runtime413.spec ~/rpmbuild/SPECS/
cp ~/pgsty/rpm/rpmbuild/SPECS/babelfish.spec ~/rpmbuild/SPECS/

cd ~/rpmbuild
make babelfish_all
```

PG18 dev source can be generated with:

```bash
bin/babelfish.sh 18.0 6.0.0 BABEL_6_X_DEV__PG_18_X BABEL_6_X_DEV
```

## Signature

All Deb Packages are signed with GPG key `9592A7BC7A682E7333376E09E7935D8DB9BD8B20` (`B9BD8B20` [Public key](KEYS))


## License

Maintainer: Ruohang Feng / [@Vonng](https://vonng.com/en/) ([rh@vonng.com](mailto:rh@vonng.com))

License: [Apache 2.0](LICENSE)
