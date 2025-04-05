# Build DocumentDB 

## EL

```bash
cp ~/rpmbuild/SOURCES/documentdb-0.102-0.tar.gz /tmp/
cd /tmp/;
tar -xf documentdb-0.102-0.tar.gz
cp -r documentdb-0.102-0/scripts /tmp/install_setup

sudo su 
# proxy env (po)

po
cd /tmp/install_setup
export CLEANUP_SETUP=1
export INSTALL_DEPENDENCIES_ROOT=/tmp/install_setup
export MAKE_PROGRAM=cmake

./install_setup_libbson.sh
./install_setup_pcre2.sh
./install_setup_intel_decimal_math_lib.sh
./install_citus_indent.sh

cd ~/rpmbuild
make documentdb
```


## Debian

```bash
cp ~/deb/tarball/documentdb-0.102-0.tar.gz /tmp/
cd /tmp/;
tar -xf documentdb-0.102-0.tar.gz
cp -r documentdb-0.102-0/scripts /tmp/install_setup

sudo su 
# proxy env (po)

po
cd /tmp/install_setup
export CLEANUP_SETUP=1
export INSTALL_DEPENDENCIES_ROOT=/tmp/install_setup
export MAKE_PROGRAM=cmake

./install_setup_libbson.sh
./install_setup_pcre2.sh
./install_setup_intel_decimal_math_lib.sh
./install_citus_indent.sh

cd ~/deb
make documentdb
```