%global sname polardb
%global pgmajorversion 17
%global pgbaseinstdir /usr/polar-%{pgmajorversion}
%global polar_commit ff510dfc
%global polar_branch POLARDB_17_STABLE
%global pgport 5432

%define _build_id_links none
%global _lto_cflags %{nil}

Name:           %{sname}-%{pgmajorversion}
Version:        17.11.1.0
Release:        1PGSTY%{?dist}
Summary:        PolarDB PostgreSQL %{pgmajorversion} kernel
License:        Apache-2.0 AND PostgreSQL AND BSD-2-Clause AND BSD-3-Clause AND MIT AND Spencer-94
URL:            https://github.com/polardb/PolarDB-for-PostgreSQL
Source0:        polardb-for-postgresql-%{version}.tar.gz
Patch0:         polardb-17.11.1.0.patch
# Bundle-style private prefix package; do not register copied libraries as system providers.
AutoReqProv:    no

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc, gcc-c++, make, readline-devel, zlib-devel >= 1.0.4
BuildRequires:  libuuid-devel, libxml2-devel, libxslt-devel, libicu-devel
BuildRequires:  openssl-devel, pam-devel, krb5-devel, openldap-devel
%if 0%{?rhel} == 8
BuildRequires:  perl-interpreter, perl-ExtUtils-Embed, perl(FindBin), perl(Opcode)
%else
BuildRequires:  perl-interpreter, perl-ExtUtils-Embed, perl-FindBin, perl-Opcode
%endif
BuildRequires:  python3-devel, tcl-devel, lz4-devel, libzstd-devel, libunwind-devel
BuildRequires:  clang, llvm-devel, file, binutils
BuildRequires:  polarstore >= 1.2.42
Requires:       tzdata
Requires(pre):  shadow-utils

%description
PolarDB for PostgreSQL %{version} is a PostgreSQL %{pgmajorversion} kernel
fork. This package ships the complete PolarDB runtime, development headers,
PGXS files, and bundled contrib extensions under %{pgbaseinstdir}.

%prep
%setup -q -n PolarDB-for-PostgreSQL-%{version}
sed -i -e 's|^POLAR_COMMIT=.*|POLAR_COMMIT="%{polar_commit}"|' configure configure.ac
sed -i -e 's|^port=$(random_unused_port)|port=%{pgport}|' build.sh
patch -p1 --fuzz=0 < %{PATCH0}
%if 0%{?rhel} == 8 && "%{_arch}" == "aarch64"
sed -i -e 's|-lpfsd -lpthread|-lpfsd -latomic -lpthread|' src/Makefile.global.in
%endif
awk '1; /  \.\/configure \$configure_flag/ { print "  (cd src/backend && MAKELEVEL=0 make submake-generated-headers)" }' build.sh > build.sh.new
mv build.sh.new build.sh
chmod +x build.sh

%build
export COPT="-Wno-error ${COPT-}"
export CC=gcc CXX=g++
export NM=gcc-nm AR=gcc-ar RANLIB=gcc-ranlib
export CLANG="${CLANG:-$(command -v clang)}"
export LLVM_CONFIG="${LLVM_CONFIG:-$(command -v llvm-config)}"
unset CFLAGS CXXFLAGS LDFLAGS

stage_root=%{_builddir}/%{name}-%{version}-stage
rm -rf "$stage_root"
mkdir -p "$stage_root"

POLAR_PACKAGE_PREFIX=%{pgbaseinstdir} DESTDIR="$stage_root" ./build.sh \
  --ec="--with-deploy-mode=opensource --with-pfsd" \
  --port=%{pgport} \
  --debug=off \
  --jobs=%{_smp_build_ncpus} \
  --ni

polar_install_dependency()
{
  stage_root=${1}
  target_dir=${2}

  cd "${stage_root}${target_dir}/lib/"
  ln -sf ../lib ./lib

  cd "$stage_root"
  binfiles=$(find "${stage_root}${target_dir}/bin")
  libfiles=$(find "${stage_root}${target_dir}/lib")
  filelist=${binfiles}$'\n'${libfiles}
  exelist=$(echo "$filelist" | xargs -r file | grep -E -v ":.* (commands|script)" | grep ":.*executable" | cut -d: -f1)
  liblist=$(echo "$filelist" | xargs -r file | grep ":.*shared object" | cut -d: -f1)

  cp /dev/null mytmpfilelist
  cp /dev/null mytmpfilelist2
  eval PERL_PATH=$(cd /usr/lib64/perl[5-9]/CORE/ 2>/dev/null && pwd || true)
  export LD_LIBRARY_PATH="${stage_root}${target_dir}/lib:$PERL_PATH:${LD_LIBRARY_PATH-}:/usr/lib64:/usr/lib"

  for f in $liblist $exelist; do
    ldd "$f" | awk '/=>/ {
      if (X$3 != "X" && $3 !~ /libNoVersion.so/ && $3 !~ /4[um]lib.so/ && $3 !~ /libredhat-kernel.so/ && $3 !~ /libselinux.so/ && $3 !~ /libjvm.so/ && $3 ~ /\.so/) {
        print $3
      }
    }' >> mytmpfilelist
  done

  sort -u mytmpfilelist > mytmpfilelist2
  while read -r line; do
    [ -n "$line" ] || continue
    ldd "$line" | awk '/=>/ {
      if (X$3 != "X" && $3 !~ /libNoVersion.so/ && $3 !~ /4[um]lib.so/ && $3 !~ /libredhat-kernel.so/ && $3 !~ /libselinux.so/ && $3 !~ /libjvm.so/ && $3 ~ /\.so/) {
        print $3
      }
    }' >> mytmpfilelist
  done < mytmpfilelist2

  sort -u mytmpfilelist > mytmpfilelist2
  while read -r line; do
    [ -n "$line" ] || continue
    base=$(basename "$line")
    dirpath="${stage_root}${target_dir}/lib"
    filepath=$dirpath/$base

    objdump -p "$line" | awk 'BEGIN { START=0; LIBNAME=""; }
      /^$/ { START=0; }
      /^Dynamic Section:$/ { START=1; }
      (START==1) && /NEEDED/ { print $2; }
      (START==2) && /^[A-Za-z]/ { START=3; }
      /^Version References:$/ { START=2; }
      (START==2) && /required from/ {
          sub(/:/, "", $3);
          LIBNAME=$3;
      }
      (START==2) && (LIBNAME!="") && ($4!="") && (($4~/^GLIBC_*/) || ($4~/^GCC_*/)) {
          print LIBNAME "(" $4 ")";
      }
      END { exit 0 }
      ' > objdumpfile

    has_private=
    if grep -q PRIVATE objdumpfile; then
      has_private=true
    fi

    if [[ ! -f $filepath && $has_private != "true" ]]; then
      cp "$line" "$dirpath"
    fi
  done < mytmpfilelist2

  rm -f mytmpfilelist mytmpfilelist2 objdumpfile
}

polar_install_dependency "$stage_root" %{pgbaseinstdir}

%install
mkdir -p %{buildroot}
cp -a "%{_builddir}/%{name}-%{version}-stage/." %{buildroot}/
for script in vacuum_maintenance.py check_unique_constraint.py dump_partition.py; do
  sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/python3|' \
    "%{buildroot}%{pgbaseinstdir}/bin/${script}"
  grep -q '^#!/usr/bin/python3$' "%{buildroot}%{pgbaseinstdir}/bin/${script}"
done

%files
%doc README.md README_zh.md HISTORY NOTICE
%license COPYRIGHT LICENSE
%{pgbaseinstdir}/*

%pre
getent group postgres >/dev/null 2>&1 || groupadd -g 26 -r postgres >/dev/null 2>&1 || groupadd -r postgres >/dev/null 2>&1 || :
getent passwd postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Sat Sep 05 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.11.1.0-1PGSTY
- Stage the install payload for standard RPM debug post-processing
- Normalize packaged Python helper shebangs for RPM BRP validation
- Use installed Perl capabilities on EL8 without switching module streams

* Mon Aug 31 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.11.1.0-1PGSTY
- Update PolarDB PostgreSQL 17 kernel to v17.11.1.0 (ff510dfc)
- Use the shared DEB/RPM package-prefix and relative-RPATH source patch

* Sun Aug 09 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.10.1.0-2PGSTY
- Require PolarStore 1.2.42 or newer and use the PGSTY package release brand

* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.10.1.0-1PIGSTY
- Add PolarDB PostgreSQL 17 kernel package under /usr/polar-17
