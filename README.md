# PGSTY RPM Package Builder

Extensions Building Scripts for PostgreSQL 13 - 18 on EL 8/9/10

- [Pigsty PGSQL Repo](https://pigsty.io/docs/repo/pgsql)
- [RPM Change Log](https://pigsty.io/docs/repo/pgsql/rpm)


## How to use?

You can build extension RPMs with [pig](https://pgext.cloud/pig).

```bash
curl https://repo.pigsty.cc/pig | bash -s 1.1.0
pig build repo
pig build tool
pig build spec # <--- get this repo, setup building environment
pig build rust
pig build pgrx

# then build packages
pig build pkg timescaledb
pig build pkg pg_search
```


## Babelfish (EL9, PG17)

Validated package chain:

1. `babelfishpg_17` (kernel)
2. `antlr4-runtime413` + `antlr4-runtime413-devel` (standalone ANTLR runtime)
3. `babelfish_extensions_17` (four core extensions)

Key files:

- `bin/babelfish.sh` (generate source tarball + ANTLR zip)
- `rpmbuild/SPECS/babelfishpg_17.spec`
- `rpmbuild/SPECS/antlr4-runtime413.spec`
- `rpmbuild/SPECS/babelfish_extensions_17.spec`
- `rpmbuild/Makefile` target: `babelfishpg`

Build on EL9 (example):

```bash
cp ~/pgsty/rpm/src/babelfishpg-17.8-5.5.0.tar.gz ~/rpmbuild/SOURCES/
cp ~/pgsty/rpm/src/antlr4-cpp-runtime-4.13.2-source.zip ~/rpmbuild/SOURCES/
cp ~/pgsty/rpm/rpmbuild/SPECS/babelfishpg_17.spec ~/rpmbuild/SPECS/
cp ~/pgsty/rpm/rpmbuild/SPECS/antlr4-runtime413.spec ~/rpmbuild/SPECS/
cp ~/pgsty/rpm/rpmbuild/SPECS/babelfish_extensions_17.spec ~/rpmbuild/SPECS/

rpmbuild -ba ~/rpmbuild/SPECS/babelfishpg_17.spec
rpmbuild -ba ~/rpmbuild/SPECS/antlr4-runtime413.spec

ARCH="$(uname -m)"
sudo dnf remove -y antlr4-runtime antlr4-runtime-devel || true
sudo dnf install -y \
  ~/rpmbuild/RPMS/${ARCH}/antlr4-runtime413-4.13.2-1PIGSTY.el9.${ARCH}.rpm \
  ~/rpmbuild/RPMS/${ARCH}/antlr4-runtime413-devel-4.13.2-1PIGSTY.el9.${ARCH}.rpm \
  ~/rpmbuild/RPMS/${ARCH}/babelfishpg_17-17.8-1PIGSTY.el9.${ARCH}.rpm

rpmbuild -ba ~/rpmbuild/SPECS/babelfish_extensions_17.spec
```


## Signature

All Deb Packages are signed with GPG key `9592A7BC7A682E7333376E09E7935D8DB9BD8B20` (`B9BD8B20` [Public key](KEYS))


## License

Maintainer: Ruohang Feng / [@Vonng](https://vonng.com/en/) ([rh@vonng.com](mailto:rh@vonng.com))

License: [Apache 2.0](LICENSE)
