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
