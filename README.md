# PGSTY/RPM: build rpm for PostgreSQL Extensions

PostgreSQL Supplementary Extensions Repository Building Specs

- PostgreSQL Extension Catalog : https://pig.pgsty.com

Related Projects:

- [`infra_pkg`](https://github.com/pgsty/infra-pkg): Building observability stack & modules from tarball
- [`rpm`](https://github.com/pgsty/rpm): Building PostgreSQL RPM packages from source code
- [`deb`](https://github.com/pgsty/deb): Building PostgreSQL DEB packages from source code
- [`pgsql-deb`](https://github.com/pgsty/pgsql-deb): Building PostgreSQL DEB packages from source code

--------

## FHS

- `rpmbuild` : the building directory that put to `~/rpmbuild` on building machine
- `yum` : the built artifact directory
- `src` : the source tarball directory


--------

## Get Started

Prepare the environment with:

```bash
curl https://repo.pigsty.cc/pig | bash -s 0.7.0
pig build spec   # <---- download the rpmbuild.tar.gz from repo
pig build repo
pig build tool
pig build rust
pig build pgrx
```

Then build specific extension with:

```bash
pig build pkg citus
pig build pkg timescaledb
pig build pkg some_other_extension....
```



--------

## License

Maintainer: Ruohang Feng / [@Vonng](https://vonng.com/en/) ([rh@vonng.com](mailto:rh@vonng.com))

License: [Apache 2.0](LICENSE)
