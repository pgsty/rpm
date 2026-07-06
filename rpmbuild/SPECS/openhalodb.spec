%global sname openhalodb
%global pgmajorversion 14
%global pgbaseinstdir	/usr/halo-%{pgmajorversion}
# Private PostgreSQL ABI under a fork prefix, not a system libpq provider.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/.*\\.so.*$
%global __requires_exclude ^(libecpg(_compat)?|libpgtypes|libpq|libpqwalreceiver)\\.so.*$

Name:		%{sname}-%{pgmajorversion}
Version:	1.0
Release:	2PIGSTY%{?dist}
Summary:	MySQL wire protocol support for PostgreSQL
License:	GPL-3.0
URL:		https://github.com/HaloTech-Co-Ltd/openHalo
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:  glibc-devel, bison >= 2.3, flex >= 2.5.35, gettext >= 0.10.35
BuildRequires:  gcc-c++, readline-devel, zlib-devel >= 1.0.4, krb5-devel
BuildRequires:  libselinux-devel >= 2.0.93, libxml2-devel, libxslt-devel, libuuid-devel
BuildRequires:  lz4-devel, libzstd-devel, libicu-devel, openldap-devel, pam-devel, python3-devel, tcl-devel
BuildRequires:  systemtap-sdt-devel, openssl-devel, systemd, systemd-devel, patchelf
%if 0%{?rhel} >= 10
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin, perl-interpreter
Requires:       systemd, lz4-libs, libzstd >= 1.5.1, /sbin/ldconfig, libicu, openssl-libs >= 3.0.0, libxml2, tzdata
%elif 0%{?rhel} == 9
BuildRequires:  perl, perl-ExtUtils-Embed, perl-FindBin
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2, tzdata
%else
BuildRequires:  perl-interpreter < 4:5.30
Requires:       systemd, lz4-libs, libzstd >= 1.4.0, /sbin/ldconfig, libicu, openssl-libs >= 1.1.1k, libxml2, tzdata
%endif
Requires(pre):  shadow-utils

%description
Adding MySQL Wire-compatibility for PostgreSQL to work with applications written for MySQL,
but provides much more better performance than MySQL!

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}.patch

%build
CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
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
--without-llvm \
--with-python \
--with-tcl \
--with-openssl \
--with-pam \
--with-gssapi \
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
make DESTDIR=%{buildroot} VERBOSE=1 %{?_smp_mflags} install-world-bin

allowed_runpath="%{pgbaseinstdir}/lib"
runpath_files=$(mktemp)
find %{buildroot}%{pgbaseinstdir} -type f > "$runpath_files"
while IFS= read -r f; do
    runpath=$(readelf -d "$f" 2>/dev/null | sed -n 's/.*(RUNPATH).*Library runpath: \[\(.*\)\].*/\1/p;s/.*(RPATH).*Library rpath: \[\(.*\)\].*/\1/p' | head -n1)
    [ -n "$runpath" ] || continue
    clean_runpath=""
    old_ifs=$IFS
    IFS=:
    for path in $runpath; do
        if [ "$path" = "$allowed_runpath" ]; then
            clean_runpath="${clean_runpath:+$clean_runpath:}$path"
        fi
    done
    IFS=$old_ifs
    if [ -n "$clean_runpath" ]; then
        [ "$clean_runpath" = "$runpath" ] || patchelf --set-rpath "$clean_runpath" "$f"
    else
        patchelf --remove-rpath "$f"
    fi
done < "$runpath_files"
rm -f "$runpath_files"

bad_runpath=$(mktemp)
find %{buildroot}%{pgbaseinstdir} -type f > "$runpath_files"
while IFS= read -r f; do
    runpath=$(readelf -d "$f" 2>/dev/null | sed -n 's/.*(RUNPATH).*Library runpath: \[\(.*\)\].*/\1/p;s/.*(RPATH).*Library rpath: \[\(.*\)\].*/\1/p' | head -n1)
    [ -z "$runpath" ] || [ "$runpath" = "$allowed_runpath" ] || echo "$f: $runpath" >> "$bad_runpath"
done < "$runpath_files"
rm -f "$runpath_files"
if [ -s "$bad_runpath" ]; then
    cat "$bad_runpath"
    rm -f "$bad_runpath"
    exit 1
fi
rm -f "$bad_runpath"

%files
%doc README.md
%license %{pgbaseinstdir}/LICENSE
%license %{pgbaseinstdir}/COPYRIGHT
%license %{pgbaseinstdir}/3party-legal-notices
%{pgbaseinstdir}/lib/*
%{pgbaseinstdir}/bin/*
%{pgbaseinstdir}/share/*
%{pgbaseinstdir}/include/*
%doc %{pgbaseinstdir}/doc/*

%pre
getent group postgres >/dev/null 2>&1 || groupadd -g 26 -r postgres >/dev/null 2>&1 || groupadd -r postgres >/dev/null 2>&1 || :
getent passwd postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || useradd -M -g postgres -r -d /var/lib/pgsql -s /bin/bash -c "PostgreSQL Server" postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.0-2PIGSTY
- Promote openhalodb to the formal 1.0 release
- Align GSSAPI support and strip non-private RUNPATH entries

* Thu Feb 26 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.0-b1PIGSTY
* Wed Apr 02 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 14.10-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
