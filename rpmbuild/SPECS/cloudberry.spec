Name:           cloudberry
Version:        2.0.0
Release:        1PIGSTY%{?dist}
Summary:        High-performance open-source data warehouse based on PostgreSQL/Greenplum

License:        Apache-2.0
URL:            https://cloudberry.apache.org
Source0:        apache-cloudberry-2.0.0-incubating-src.tar.gz
Prefix:         /usr/local

# Cloudberry includes many ELF/GO binaries; do not fail hard on missing build-id edge cases.
%define _missing_build_ids_terminate_build 0
# Disable debuginfo/debugsource subpackages for this monolithic upstream build.
%global debug_package %{nil}
# Skip generating debugsource package content.
%define _debugsource_template %{nil}

BuildRequires:  apr-devel
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  krb5-devel
BuildRequires:  libcurl-devel
BuildRequires:  libevent-devel
BuildRequires:  libicu-devel
BuildRequires:  libuv-devel
BuildRequires:  libxml2-devel
BuildRequires:  libyaml-devel
BuildRequires:  libzstd-devel
BuildRequires:  lz4-devel
BuildRequires:  make
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  protobuf-devel >= 3.5.0
BuildRequires:  protobuf-compiler
BuildRequires:  perl
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  xerces-c-devel
BuildRequires:  zlib-devel

Requires:       apr
Requires:       bash
Requires:       bzip2
Requires:       iproute
Requires:       iputils
%if 0%{?rhel} <= 8
Requires:       keyutils
%endif
Requires:       libcurl
Requires:       libevent
Requires:       libidn2
Requires:       libstdc++
Requires:       libuv
Requires:       libxml2
Requires:       libyaml
Requires:       libzstd
Requires:       lz4
Requires:       openldap
Requires:       openssh
Requires:       openssh-clients
Requires:       openssh-server
Requires:       pam
Requires:       perl
Requires:       python3
Requires:       readline
Requires:       rsync
Requires(pre):  shadow-utils

%description
Cloudberry is an advanced, open-source, massively parallel processing (MPP)
data warehouse developed from PostgreSQL and Greenplum.

%prep
%setup -q -n apache-cloudberry-2.0.0-incubating
%if 0%{?rhel} >= 10
# On EL10/OpenSSL3 builds, USE_SSL_ENGINE is disabled, so this variable becomes
# unused and fails under global -Werror. Keep declaration scoped to engine path.
sed -i 's/^\([[:space:]]*EVP_PKEY[[:space:]]*\*pkey = NULL;\)$/#ifdef USE_SSL_ENGINE\
\1\
#endif/' src/interfaces/libpq/fe-secure-openssl.c
# GCC 14 may treat alt_name as potentially uninitialized in SAN iteration.
sed -i 's/char[[:space:]]*\*alt_name;/char       *alt_name = NULL;/' \
  src/interfaces/libpq/fe-secure-openssl.c
# GCC 14 treats overload hiding as error under gporca's -Werror settings.
sed -i '0,/^[[:space:]]*public:[[:space:]]*$/s//public:\
\tusing CWStringBase::Equals;/' \
  src/backend/gporca/libgpos/include/gpos/string/CWStringConst.h
# libxml2 on EL10 uses const xmlError * in xmlStructuredErrorFunc callback.
sed -i 's/xmlErrorPtr error/const xmlError *error/g' src/backend/utils/adt/xml.c
# Fix ORCA static initialization order bug that can crash at process start on EL10:
# CMDIdGPDB ctor references m_mdid_invalid_key during global initialization.
sed -i 's/if (CMDIdGPDB::m_mdid_invalid_key.Oid() == oid)/if (0 == oid)/g' \
  src/backend/gporca/libnaucrates/src/md/CMDIdGPDB.cpp
# EL10 toolchain (gcc14/libxml2/OpenSSL3) triggers many legacy warnings.
# Build cloudberry with warnings enabled but not fatal.
sed -i 's/^CUSTOM_COPT += -Werror/CUSTOM_COPT += -Wno-error/' src/Makefile.custom
sed -i 's/override CXXFLAGS := -Werror /override CXXFLAGS := -Wno-error /' \
  src/backend/gporca/gporca.mk
sed -i 's/ -Werror / -Wno-error /g' contrib/pax_storage/CMakeLists.txt
sed -i 's/BENCHMARK_ENABLE_WERROR "Build Release candidates with -Werror." ON/BENCHMARK_ENABLE_WERROR "Build Release candidates with -Werror." OFF/' \
  contrib/pax_storage/src/cpp/contrib/googlebench/CMakeLists.txt
sed -i 's/add_cxx_compiler_flag(-Werror)/add_cxx_compiler_flag(-Wno-error)/g' \
  contrib/pax_storage/src/cpp/contrib/googlebench/CMakeLists.txt
%endif
%if 0%{?rhel} <= 8
# EL8/GCC8 fails benchmark regex probes when unknown -Wno-* meets inherited -Werror.
sed -i 's/ -Werror / -Wno-error /g' contrib/pax_storage/CMakeLists.txt
sed -i 's/-Wno-redundant-move -Wno-error=redundant-move //g' contrib/pax_storage/CMakeLists.txt
sed -i 's/option(BUILD_GTEST \"Build with google test\" ON)/option(BUILD_GTEST \"Build with google test\" OFF)/' \
  contrib/pax_storage/CMakeLists.txt
sed -i 's/option(BUILD_GBENCH \"Build with google benchmark\" ON)/option(BUILD_GBENCH \"Build with google benchmark\" OFF)/' \
  contrib/pax_storage/CMakeLists.txt
sed -i 's/BENCHMARK_ENABLE_WERROR "Build Release candidates with -Werror." ON/BENCHMARK_ENABLE_WERROR "Build Release candidates with -Werror." OFF/' \
  contrib/pax_storage/src/cpp/contrib/googlebench/CMakeLists.txt
sed -i 's/add_cxx_compiler_flag(-Werror)/add_cxx_compiler_flag(-Wno-error)/g' \
  contrib/pax_storage/src/cpp/contrib/googlebench/CMakeLists.txt
%endif

%build
./configure \
  --prefix=/usr/local/cloudberry-2.0.0 \
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

make DESTDIR=%{buildroot} install
# Keep non-versioned symlink /usr/local/cloudberry usable:
# source /usr/local/cloudberry/greenplum_path.sh must resolve absolute GPHOME.
sed -i 's/GPHOME=$(readlink "${SCRIPT_DIR}")/GPHOME=$(readlink -f "${SCRIPT_DIR}")/' \
  %{buildroot}/usr/local/cloudberry-2.0.0/greenplum_path.sh
# gpMgmt python extensions can retain buildroot include paths in DWARF;
# strip debug info to pass check-buildroot while keeping runtime symbols.
find %{buildroot}/usr/local/cloudberry-2.0.0/lib/python -type f -name '*.so' \
  -exec %{__strip} --strip-debug {} + || true
install -Dpm 0644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE

mkdir -p %{buildroot}/usr/local
ln -sfn cloudberry-2.0.0 %{buildroot}/usr/local/cloudberry

%files
/usr/local/cloudberry-2.0.0
/usr/local/cloudberry
%license /usr/share/licenses/%{name}/LICENSE

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
  if [ "$(readlink -f /usr/local/cloudberry)" = "/usr/local/cloudberry-2.0.0" ]; then
    unlink /usr/local/cloudberry || true
  fi
fi

%changelog
* Fri Feb 20 2026 Ruohang Feng <rh@vonng.com> - 2.0.0-1PIGSTY
- Initial RPM package for Apache Cloudberry 2.0.0 (incubating)
