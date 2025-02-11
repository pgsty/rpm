#!/bin/bash


## EL

```bash
# el8
sudo dnf install -y https://apache.jfrog.io/artifactory/arrow/almalinux/8/apache-arrow-release-latest.rpm
sudo dnf install -y https://packages.groonga.org/almalinux/8/groonga-release-latest.noarch.rpm

# el9
sudo dnf install -y https://apache.jfrog.io/artifactory/arrow/almalinux/9/apache-arrow-release-latest.rpm
sudo dnf install -y https://packages.groonga.org/almalinux/9/groonga-release-latest.noarch.rpm


yum download arrow-devel-18.0.0
yum download arrow1800-libs-18.0.0
yum download groonga-devel
yum download groonga-libs
yum download groonga-tokenizer-mecab

sudo yum install arrow-devel-18.0.0
sudo yum install groonga-devel
sudo dnf install ccache llvm-toolset llvm-devel msgpack-devel xxhash-devel
```



## Debian

```bash
# debian
wget https://packages.groonga.org/debian/groonga-apt-source-latest-$(lsb_release --codename --short).deb
sudo apt install -y -V ./groonga-apt-source-latest-$(lsb_release --codename --short).deb

# ubuntu
sudo add-apt-repository -y ppa:groonga/ppa

# install dependencies
sudo apt install libgroonga-dev libmsgpack-dev
```





## Source

```bash
cd vendor
git clone git@github.com:Cyan4973/xxHash.git
```
