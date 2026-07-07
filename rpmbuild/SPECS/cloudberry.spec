Name:           cloudberry
Version:        2.1.0
Release:        3PIGSTY%{?dist}
Summary:        High-performance open-source data warehouse based on PostgreSQL/Greenplum

License:        Apache-2.0
URL:            https://cloudberry.apache.org
Source0:        apache-cloudberry-2.1.0-incubating-src.tar.gz
Source1:        psutil-5.7.0.tar.gz
Source2:        PyGreSQL-5.2.tar.gz
Source3:        PyYAML-5.4.1.tar.gz
Source4:        cloudberry-2.1.0-rpm-patches.tar.gz
Source5:        Cython-0.29.37.tar.gz
%global cb_prefix /usr/cloudberry
# Private PostgreSQL ABI under a fork prefix, not a system libpq provider.
%global __provides_exclude_from ^%{cb_prefix}/lib(64)?/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver|libpostgres|libgppc|libpaxformat)\\.so.*$

# Cloudberry includes many ELF/GO binaries; do not fail hard on missing build-id edge cases.
%define _missing_build_ids_terminate_build 0
%define _build_id_links none
# LTO trips fatal warnings in the bundled PAX C++ code; keep the kernel build non-LTO.
%global _lto_cflags %{nil}
# Disable debuginfo/debugsource subpackages for this monolithic upstream build.
%global debug_package %{nil}
# Skip generating debugsource package content.
%define _debugsource_template %{nil}

BuildRequires:  apr-devel bison bzip2-devel cmake curl flex gcc gcc-c++ krb5-devel libcurl-devel libevent-devel libicu-devel liburing-devel libuuid-devel libuv-devel libxml2-devel libyaml-devel libzstd-devel lz4-devel make openldap-devel openssl-devel pam-devel perl perl-devel perl-ExtUtils-Embed protobuf-devel >= 3.5.0 protobuf-compiler python3-Cython python3-devel python3-pip python3-setuptools python3-wheel readline-devel xerces-c-devel zlib-devel
Requires:       apr bash bzip2 iproute iputils libcurl libevent libidn2 libstdc++ liburing libuuid libuv libxml2 libyaml libzstd lz4 openldap openssh openssh-clients openssh-server pam perl python3 readline rsync /sbin/ldconfig

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
patch -p1 --forward -f < .rpm-patches/cloudberry-2.1.0-initdb-cdb-initd-errno.patch
%if 0%{?rhel} >= 10
patch -p1 --forward -f < .rpm-patches/cloudberry-2.1.0-el10-build-fixes.patch
%endif
%if 0%{?rhel} <= 9
patch -p1 --forward -f < .rpm-patches/cloudberry-2.1.0-el8-pax-storage-build-fixes.patch
%endif
mkdir -p gpMgmt/bin/pythonSrc/ext
# Pre-seed gpMgmt Python sdists so make install stays reproducible and offline.
cp -fp %{SOURCE1} gpMgmt/bin/pythonSrc/ext/
cp -fp %{SOURCE2} gpMgmt/bin/pythonSrc/ext/
cp -fp %{SOURCE3} gpMgmt/bin/pythonSrc/ext/
cp -fp %{SOURCE5} gpMgmt/bin/pythonSrc/ext/
sed -i 's|pip3 install --user wheel "cython<3.0.0"|pip3 install --user wheel $(PYLIB_SRC_EXT)/Cython-0.29.37.tar.gz|' gpMgmt/bin/Makefile

%build
CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo $CFLAGS | xargs -n 1 | grep -Ev '^-ffast-math$|^-flto(=.*)?$|^-ffat-lto-objects$' | xargs -n 100`
CFLAGS="$CFLAGS -Wno-error=date-time -Wno-error=stringop-overflow -Wno-error=maybe-uninitialized -Wno-error=array-bounds"
CXXFLAGS="${CXXFLAGS:-%optflags}"
CXXFLAGS=`echo $CXXFLAGS | xargs -n 1 | grep -Ev '^-ffast-math$|^-flto(=.*)?$|^-ffat-lto-objects$' | xargs -n 100`
CXXFLAGS="$CXXFLAGS -Wno-error=date-time -Wno-error=stringop-overflow -Wno-error=maybe-uninitialized -Wno-error=array-bounds -Wno-error=pessimizing-move -Wno-error=suggest-attribute=format -Wno-error=overloaded-virtual"
PG_CXXFLAGS="${PG_CXXFLAGS:-} -Wno-error=overloaded-virtual"
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
export CFLAGS CXXFLAGS PG_CXXFLAGS

./configure \
  --enable-rpath \
  --prefix=%{cb_prefix} \
  --bindir=%{cb_prefix}/bin \
  --includedir=%{cb_prefix}/include \
  --mandir=%{cb_prefix}/share/man \
  --datadir=%{cb_prefix}/share \
  --libdir=%{cb_prefix}/lib \
  --docdir=%{cb_prefix}/doc \
  --htmldir=%{cb_prefix}/doc/html \
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
  --with-uuid=e2fs \
  --with-includes=/usr/include/xercesc \
  --with-libraries=%{_libdir}

# Avoid a parallel build race where src/common may include utils/errcodes.h
# before it is generated.
MAKELEVEL=0 %{__make} -C src/backend submake-generated-headers
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin
MAKELEVEL=0 %{__make} %{?_smp_mflags} -C contrib

%install
rm -rf %{buildroot}
# Cloudberry carries a private RPATH to %{cb_prefix}/lib.
export QA_RPATHS=3
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_INDEX=1

install -dpm 0755 %{buildroot}%{cb_prefix}/share/postgresql/cdb_init.d
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} -C contrib install
# gpMgmt python extensions can retain buildroot include paths in DWARF;
# strip debug info to pass check-buildroot while keeping runtime symbols.
[ ! -d %{buildroot}%{cb_prefix}/lib/python ] || find %{buildroot}%{cb_prefix}/lib/python -type f -name '*.so' \
  -exec %{__strip} --strip-debug {} + || true
install -Dpm 0644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -Dpm 0644 NOTICE %{buildroot}%{_docdir}/%{name}/NOTICE

bad_runpath=$(mktemp)
local_prefix=/usr/local
find %{buildroot}%{cb_prefix} -type f | while IFS= read -r f; do
  runpath=$(readelf -d "$f" 2>/dev/null | sed -n 's/.*(RUNPATH).*Library runpath: \[\(.*\)\].*/\1/p;s/.*(RPATH).*Library rpath: \[\(.*\)\].*/\1/p' | head -n1)
  [ -n "$runpath" ] || continue
  case "$runpath" in
    *%{buildroot}*|*${local_prefix}/cloudberry*|*/root/rpmbuild*)
      echo "$f: $runpath" >> "$bad_runpath"
      ;;
  esac
done
if [ -s "$bad_runpath" ]; then
  cat "$bad_runpath"
  rm -f "$bad_runpath"
  exit 1
fi
rm -f "$bad_runpath"

%files
%{cb_prefix}
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
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Tue Jul 07 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-3PIGSTY
- Move the RPM payload to /usr/cloudberry to match the DEB package
- Standardize private-prefix CFLAGS, LDFLAGS, RPATH, and ABI filtering

* Sun Apr 19 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-2PIGSTY
- Reset errno before scanning cdb_init.d so initdb no longer misreports ENOSYS
- Rebuild EL10 packages after fixing the runtime initdb failure

* Thu Apr 16 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Upgrade Apache Cloudberry to 2.1.0 (incubating)
- Track source-level packaging fixes as reusable patch files
- Pre-seed gpMgmt Python sources for offline RPM builds and package NOTICE
- Pre-seed Cython 0.29.37 so EL10 gpMgmt install stays offline-compatible

* Fri Feb 20 2026 Ruohang Feng <rh@vonng.com> - 2.0.0-1PIGSTY
- Initial RPM package for Apache Cloudberry 2.0.0 (incubating)
