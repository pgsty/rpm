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


```bash
apt -y install patchelf
```


## pg_duckdb build

```bash
if [[ ${OS_VERSION} == "12" ]]; then
    log_info "install deb12 utils"
    sudo apt install -y lz4 unzip wget patch bash lsof sshpass debhelper devscripts fakeroot pkg-config make cmake ncdu rsync #build-essential
    sudo apt install -y postgresql-all postgresql-server-dev-all libreadline-dev flex bison libxml2-dev libxml2-utils xsltproc libc++-dev libc++abi-dev libglib2.0-dev libtinfo5 libstdc++-12-dev liblz4-dev ninja-build
elif [[ ${OS_VERSION} == "22" ]]; then
    log_info "install ubuntu22 utils"
    sudo apt install -y lz4 unzip wget patch bash lsof sshpass debhelper devscripts fakeroot pkg-config make cmake ncdu rsync #build-essential
    sudo apt install -y postgresql-all postgresql-server-dev-all libreadline-dev flex bison libxml2-dev libxml2-utils xsltproc libc++-dev libc++abi-dev libglib2.0-dev libtinfo6 libstdc++-12-dev liblz4-dev ninja-build
elif [[ ${OS_VERSION} == "24" ]]; then
    log_info "install ubuntu24 utils"
    sudo apt install -y lz4 unzip wget patch bash lsof sshpass debhelper devscripts fakeroot pkg-config make cmake ncdu rsync #build-essential
    sudo apt install -y postgresql-all postgresql-server-dev-all libreadline-dev flex bison libxml2-dev libxml2-utils xsltproc libc++-dev libc++abi-dev libglib2.0-dev libtinfo6 libstdc++-12-dev liblz4-dev ninja-build
fi
```