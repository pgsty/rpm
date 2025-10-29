


## EL10

```bash
cat > /etc/yum.repos.d/groonga.repo <<-'EOF'
[apache-arrow-almalinux]
name=Apache Arrow for AlmaLinux $releasever - $basearch
baseurl=https://apache.jfrog.io/artifactory/arrow/almalinux/$releasever/$basearch/
gpgcheck=0
enabled=1

[groonga-almalinux]
name=The Groonga Project for AlmaLinux $releasever - $basearch
baseurl=https://packages.groonga.org/almalinux/$releasever/$basearch/
gpgcheck=0
enabled=1
EOF

cat /etc/yum.repos.d/groonga.repo
yum makecache
```

```bash
yum download arrow2100-libs arrow2100-compute-libs arrow-devel-21.0.0*

dnf download arrow-compute-devel-21*
```


##









#!/bin/bash



```bash
curl https://repo.pigsty.cc/pig | bash
```

```bash
pig repo set -u
yum install -y scws
apt install -y scws
```

## EL

```bash
# el8
sudo dnf install -y https://apache.jfrog.io/artifactory/arrow/almalinux/8/apache-arrow-release-latest.rpm
sudo dnf install -y https://packages.groonga.org/almalinux/8/groonga-release-latest.noarch.rpm

# el9
sudo dnf install -y https://apache.jfrog.io/artifactory/arrow/almalinux/9/apache-arrow-release-latest.rpm
sudo dnf install -y https://packages.groonga.org/almalinux/9/groonga-release-latest.noarch.rpm


#yum download arrow-devel-18.0.0
#yum download arrow1800-libs-18.0.0
#yum download groonga-devel
#yum download groonga-libs
#yum download groonga-tokenizer-mecab

sudo yum install -y groonga-devel
sudo dnf install -y ccache llvm-toolset llvm-devel msgpack-devel xxhash-devel
```



## Debian

```bash
# debian
wget https://packages.groonga.org/debian/groonga-apt-source-latest-$(lsb_release --codename --short).deb
sudo apt install -y -V ./groonga-apt-source-latest-$(lsb_release --codename --short).deb

# ubuntu
sudo add-apt-repository -y ppa:groonga/ppa

# install dependencies
sudo apt install -y libgroonga-dev libmsgpack-dev
```

Download libgronnga0:

```bash
apt download libgronnga0
```


- Debian:
  - groonga: https://packages.groonga.org/debian/ 
  - arrow: https://apache.jfrog.io/artifactory/arrow/debian/ 
- Ubuntu: https://ppa.launchpadcontent.net/groonga/ppa/ubuntu/pool/main/g/groonga/
- EL: 
  - groonga: https://packages.groonga.org/almalinux/
  - arrow: https://apache.jfrog.io/artifactory/arrow/almalinux/


```bash
https://apache.jfrog.io/ui/native/arrow/almalinux/8/aarch64/Packages/arrow1900-libs-19.0.0-1.el8.aarch64.rpm
https://apache.jfrog.io/ui/native/arrow/almalinux/8/aarch64/Packages/arrow-devel-19.0.0-1.el8.aarch64.rpm
https://apache.jfrog.io/ui/native/arrow/almalinux/8/x86_64/Packages/arrow1900-libs-19.0.0-1.el8.x86_64.rpm
https://apache.jfrog.io/ui/native/arrow/almalinux/8/x86_64/Packages/arrow-devel-19.0.0-1.el8.x86_64.rpm

https://apache.jfrog.io/ui/native/arrow/almalinux/9/aarch64/Packages/arrow1900-libs-19.0.0-1.el9.aarch64.rpm
https://apache.jfrog.io/ui/native/arrow/almalinux/9/aarch64/Packages/arrow-devel-19.0.0-1.el9.aarch64.rpm
https://apache.jfrog.io/ui/native/arrow/almalinux/9/x86_64/Packages/arrow1900-libs-19.0.0-1.el9.x86_64.rpm
https://apache.jfrog.io/ui/native/arrow/almalinux/9/x86_64/Packages/arrow-devel-19.0.0-1.el9.x86_64.rpm
```

## Source

```bash
cd vendor
git clone git@github.com:Cyan4973/xxHash.git
```
