# pg_mooncake build


```bash
yum install patchelf
```

```bash
cd ~/rpmbuild/SOURCES
tar -xf pg_mooncake-0.1.2.tar.gz
vi pg_mooncake-0.1.2/src/pgduckdb/scan/postgres_seq_scan.cpp

75G dd dd j dd :q

tar -zcf pg_mooncake-0.1.2.tar.gz pg_mooncake-0.1.2
rm -rf pg_mooncake-0.1.2
```