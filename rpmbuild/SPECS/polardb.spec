%global sname polardb
%global pgmajorversion 17
%global pgbaseinstdir /usr/polar-%{pgmajorversion}
%global polar_commit accf02e2
%global polar_branch POLARDB_17_STABLE
%global pgport 5432

%define debug_package %{nil}
%define _build_id_links none
%define __os_install_post %{nil}
%global _lto_cflags %{nil}

Name:           %{sname}-%{pgmajorversion}
Version:        17.10.1.0
Release:        1PIGSTY%{?dist}
Summary:        PolarDB PostgreSQL %{pgmajorversion} kernel
License:        Apache-2.0 AND PostgreSQL
URL:            https://github.com/polardb/PolarDB-for-PostgreSQL
Source0:        polardb-for-postgresql-%{version}.tar.gz
AutoReqProv:    no

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc, gcc-c++, make, readline-devel, zlib-devel >= 1.0.4
BuildRequires:  libuuid-devel, libxml2-devel, libxslt-devel, libicu-devel
BuildRequires:  openssl-devel, pam-devel, krb5-devel, openldap-devel
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin, perl-interpreter
BuildRequires:  python3-devel, tcl-devel, lz4-devel, libzstd-devel, libunwind-devel
BuildRequires:  clang, llvm-devel, file, binutils
Requires(pre):  shadow-utils

%description
PolarDB for PostgreSQL %{version} is a PostgreSQL %{pgmajorversion} kernel
fork. This package ships the complete PolarDB runtime, development headers,
PGXS files, and bundled contrib extensions under %{pgbaseinstdir}.

%prep
%setup -q -n PolarDB-for-PostgreSQL-%{version}
sed -i -e 's|^POLAR_COMMIT=.*|POLAR_COMMIT="%{polar_commit}"|' configure configure.ac
sed -i -e 's|^port=$(random_unused_port)|port=%{pgport}|' build.sh
awk '1; /  \.\/configure \$configure_flag/ { print "  (cd src/backend && MAKELEVEL=0 make submake-generated-headers)" }' build.sh > build.sh.new
mv build.sh.new build.sh
chmod +x build.sh

%build
export COPT="-Wno-error ${COPT-}"
export CC=gcc CXX=g++
export NM=gcc-nm AR=gcc-ar RANLIB=gcc-ranlib
export CLANG="${CLANG:-$(command -v clang)}"
export LLVM_CONFIG="${LLVM_CONFIG:-$(command -v llvm-config)}"

DESTDIR=%{buildroot} ./build.sh \
  --ec="--prefix=%{pgbaseinstdir} --with-deploy-mode=opensource --with-pfsd" \
  --port=%{pgport} \
  --debug=off \
  --jobs=%{_smp_build_ncpus} \
  --ni

polar_install_dependency()
{
  target_dir=${1}

  cd %{buildroot}${target_dir}/lib/
  ln -sf ../lib ./lib

  cd %{buildroot}
  binfiles=$(find %{buildroot}${target_dir}/bin)
  libfiles=$(find %{buildroot}${target_dir}/lib)
  filelist=${binfiles}$'\n'${libfiles}
  exelist=$(echo "$filelist" | xargs -r file | grep -E -v ":.* (commands|script)" | grep ":.*executable" | cut -d: -f1)
  liblist=$(echo "$filelist" | xargs -r file | grep ":.*shared object" | cut -d: -f1)

  cp /dev/null mytmpfilelist
  cp /dev/null mytmpfilelist2
  eval PERL_PATH=$(cd /usr/lib64/perl[5-9]/CORE/ 2>/dev/null && pwd || true)
  export LD_LIBRARY_PATH=%{buildroot}${target_dir}/lib:$PERL_PATH:${LD_LIBRARY_PATH-}:/usr/lib64:/usr/lib

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
    dirpath=%{buildroot}${target_dir}/lib
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

polar_install_dependency %{pgbaseinstdir}

%files
%doc README.md README_zh.md HISTORY NOTICE
%license COPYRIGHT LICENSE
%{pgbaseinstdir}/*

%pre
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.10.1.0-1PIGSTY
- Add PolarDB PostgreSQL 17 kernel package under /usr/polar-17
