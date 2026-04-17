Name:           cloudberry
Version:        2.1.0
Release:        1PIGSTY%{?dist}
Summary:        High-performance open-source data warehouse based on PostgreSQL/Greenplum

License:        Apache-2.0
URL:            https://cloudberry.apache.org
Source0:        apache-cloudberry-2.1.0-incubating-src.tar.gz
Source1:        psutil-5.7.0.tar.gz
Source2:        PyGreSQL-5.2.tar.gz
Source3:        PyYAML-5.4.1.tar.gz
Source4:        cloudberry-2.1.0-rpm-patches.tar.gz
Prefix:         /usr/local

# Cloudberry includes many ELF/GO binaries; do not fail hard on missing build-id edge cases.
%define _missing_build_ids_terminate_build 0
# Disable debuginfo/debugsource subpackages for this monolithic upstream build.
%global debug_package %{nil}
# Skip generating debugsource package content.
%define _debugsource_template %{nil}

BuildRequires:  apr-devel bison bzip2-devel cmake curl flex gcc gcc-c++ krb5-devel libcurl-devel libevent-devel libicu-devel liburing-devel libuuid-devel libuv-devel libxml2-devel libyaml-devel libzstd-devel lz4-devel make openldap-devel openssl-devel pam-devel perl perl-devel perl-ExtUtils-Embed protobuf-devel >= 3.5.0 protobuf-compiler python3-Cython python3-devel python3-pip python3-setuptools python3-wheel readline-devel xerces-c-devel zlib-devel
Requires:       apr bash bzip2 iproute iputils libcurl libevent libidn2 libstdc++ liburing libuuid libuv libxml2 libyaml libzstd lz4 openldap openssh openssh-clients openssh-server pam perl python3 readline rsync

%if 0%{?rhel} <= 8
Requires:       keyutils
%endif

Requires(pre):  shadow-utils

%description
Cloudberry is an advanced, open-source, massively parallel processing (MPP)
data warehouse developed from PostgreSQL and Greenplum.

%prep
%setup -q -n apache-cloudberry-2.1.0-incubating
mkdir -p .rpm-patches
tar -xzf %{SOURCE4} -C .rpm-patches
patch -p1 --forward -f < .rpm-patches/cloudberry-2.1.0-env-symlink.patch
%if 0%{?rhel} >= 10
patch -p1 --forward -f < .rpm-patches/cloudberry-2.1.0-el10-build-fixes.patch
%endif
%if 0%{?rhel} <= 8
patch -p1 --forward -f < .rpm-patches/cloudberry-2.1.0-el8-pax-storage-build-fixes.patch
%endif
mkdir -p gpMgmt/bin/pythonSrc/ext
# Pre-seed gpMgmt Python sdists so make install stays reproducible and offline.
cp -fp %{SOURCE1} gpMgmt/bin/pythonSrc/ext/
cp -fp %{SOURCE2} gpMgmt/bin/pythonSrc/ext/
cp -fp %{SOURCE3} gpMgmt/bin/pythonSrc/ext/

%build
./configure \
  --prefix=/usr/local/cloudberry-2.1.0 \
  --disable-external-fts \
  --enable-gpcloud \
  --enable-ic-proxy \
  --enable-mapreduce \
  --enable-orafce \
  --enable-orca \
  --enable-pax \
  --disable-pxf \
  --disable-tap-tests \
  --with-gssapi \
  --with-ldap \
  --with-libxml \
  --with-lz4 \
  --with-openssl \
  --with-pam \
  --with-perl \
  --with-pgport=5432 \
  --with-python \
  --with-pythonsrc-ext \
  --with-ssl=openssl \
  --with-uuid=e2fs

# Avoid a parallel build race where src/common may include utils/errcodes.h
# before it is generated.
make -C src/backend MAKELEVEL=0 submake-generated-headers
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%if 0%{?rhel} >= 10
# EL10 check-rpaths hits Cloudberry's custom RUNPATHs:
# 0001 standard path, 0002 custom absolute path, 0008 $ORIGIN ordering.
export QA_RPATHS=$((0x0001|0x0002|0x0008))
%endif
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_INDEX=1

make DESTDIR=%{buildroot} install
# gpMgmt python extensions can retain buildroot include paths in DWARF;
# strip debug info to pass check-buildroot while keeping runtime symbols.
find %{buildroot}/usr/local/cloudberry-2.1.0/lib/python -type f -name '*.so' \
  -exec %{__strip} --strip-debug {} + || true
install -Dpm 0644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -Dpm 0644 NOTICE %{buildroot}%{_docdir}/%{name}/NOTICE

mkdir -p %{buildroot}/usr/local
ln -sfn cloudberry-2.1.0 %{buildroot}/usr/local/cloudberry

%files
/usr/local/cloudberry-2.1.0
/usr/local/cloudberry
%license /usr/share/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/NOTICE

%pre
if ! getent group gpadmin >/dev/null 2>&1; then
    %{_sbindir}/groupadd -r gpadmin
fi
if ! id gpadmin >/dev/null 2>&1; then
    %{_sbindir}/useradd -r -m -g gpadmin -d /home/gpadmin -s /bin/bash gpadmin
fi

%post

%postun
if [ $1 -eq 0 ] ; then
  if [ "$(readlink -f /usr/local/cloudberry)" = "/usr/local/cloudberry-2.1.0" ]; then
    unlink /usr/local/cloudberry || true
  fi
fi

%changelog
* Thu Apr 16 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Upgrade Apache Cloudberry to 2.1.0 (incubating)
- Track source-level packaging fixes as reusable patch files
- Pre-seed gpMgmt Python sources for offline RPM builds and package NOTICE

* Fri Feb 20 2026 Ruohang Feng <rh@vonng.com> - 2.0.0-1PIGSTY
- Initial RPM package for Apache Cloudberry 2.0.0 (incubating)
