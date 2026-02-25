%global sname pgedge
%global pgmajorversion 17
%global pgversion 17.7
%global spockversion 5.0.5
%global pgbaseinstdir /usr/pgedge-%{pgmajorversion}

Name:           %{sname}_%{pgmajorversion}
Version:        %{pgversion}
Release:        1PIGSTY%{?dist}
Summary:        pgEdge PostgreSQL kernel with Spock patchset
License:        PostgreSQL
URL:            https://github.com/pgEdge/spock
Source0:        postgresql-%{pgversion}.tar.gz
Source1:        spock-%{spockversion}.tar.gz

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4, clang, llvm, clang-devel, llvm-devel
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2
Requires(pre):  shadow-utils

%description
pgEdge patched PostgreSQL %{pgmajorversion} kernel package.
This package installs PostgreSQL binaries and libraries under %{pgbaseinstdir}.

%prep
%setup -q -n postgresql-%{pgversion}

rm -rf .spock-src
mkdir -p .spock-src
tar -xzf %{SOURCE1} -C .spock-src

spock_src=$(find .spock-src -mindepth 1 -maxdepth 1 -type d | head -n 1)
if [ -z "$spock_src" ]; then
  echo "cannot locate extracted spock source tree" >&2
  exit 1
fi

if [ -d "$spock_src/patches/pg%{pgmajorversion}" ]; then
  patch_dir="$spock_src/patches/pg%{pgmajorversion}"
elif [ -d "$spock_src/patches/%{pgmajorversion}" ]; then
  patch_dir="$spock_src/patches/%{pgmajorversion}"
else
  echo "cannot locate spock patches for PG%{pgmajorversion}" >&2
  exit 1
fi

for patch_name in $(ls -1 "$patch_dir" | sort); do
  patch -p1 < "$patch_dir/$patch_name"
done

%build
CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo $CFLAGS | xargs -n 1 | grep -v ffast-math | xargs -n 100`
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
export CFLAGS

./configure --enable-rpath \
--prefix=%{pgbaseinstdir} \
--includedir=%{pgbaseinstdir}/include \
--mandir=%{pgbaseinstdir}/share/man \
--datadir=%{pgbaseinstdir}/share \
--libdir=%{pgbaseinstdir}/lib \
--docdir=%{pgbaseinstdir}/doc \
--htmldir=%{pgbaseinstdir}/doc/html \
--with-system-tzdata=/usr/share/zoneinfo \
--with-lz4 \
--with-zstd \
--with-uuid=e2fs \
--with-libxml \
--with-libxslt \
--with-icu \
--with-llvm \
--with-python \
--with-tcl \
--with-openssl \
--with-pam \
--with-ldap \
--with-selinux \
--with-systemd \
--with-includes=/usr/include \
--with-libraries=%{_libdir} \
--enable-nls \
--enable-dtrace

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin

%files
%doc README.md
%license COPYRIGHT
%{pgbaseinstdir}/lib/*
%{pgbaseinstdir}/bin/*
%{pgbaseinstdir}/share/*
%{pgbaseinstdir}/include/*
%doc %{pgbaseinstdir}/doc/*

%pre
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Tue Feb 24 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 17.7-1PIGSTY
- Build pgEdge PostgreSQL kernel package and apply Spock PG17 patchset in prep stage
