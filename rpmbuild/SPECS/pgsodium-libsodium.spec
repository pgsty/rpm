%global _lto_cflags %{nil}
%global private_prefix pgsodium_private_
%global private_includedir /usr/include/pgsodium-libsodium
%global private_libdir /usr/lib/pgsodium-libsodium

Name:           pgsodium-libsodium-devel
Version:        1.0.22
Release:        1PGSTY%{?dist}
Summary:        Private symbol-prefixed libsodium for building pgsodium
License:        ISC
URL:            https://github.com/jedisct1/libsodium
Source0:        https://download.libsodium.org/libsodium/releases/libsodium-%{version}.tar.gz

BuildRequires:  binutils gcc make

%description
PIC static libsodium archive and private headers for pgsodium. Every defined
symbol is renamed with a pgsodium_private_ prefix so the resulting PostgreSQL
extension cannot interpose with the operating system libsodium ABI.

%prep
%setup -q -n libsodium-%{version}

%build
./configure --disable-shared --enable-static --with-pic --prefix=/usr \
  CFLAGS="%{optflags} -fPIC"
%{__make} %{?_smp_mflags}
mkdir -p .pgsodium-private
LC_ALL=C nm -g --defined-only -P src/libsodium/.libs/libsodium.a | \
  awk '$1 ~ /^[A-Za-z_][A-Za-z0-9_]*$/ { print $1 }' | sort -u \
  > .pgsodium-private/symbols.txt
test "$(wc -l < .pgsodium-private/symbols.txt)" -gt 700
awk '{ print $1, "%{private_prefix}" $1 }' \
  .pgsodium-private/symbols.txt > .pgsodium-private/redefine.syms
objcopy --redefine-syms=.pgsodium-private/redefine.syms \
  src/libsodium/.libs/libsodium.a .pgsodium-private/libsodium-pgsodium.a
{
  echo '#ifndef PGSODIUM_LIBSODIUM_SYMBOLS_H'
  echo '#define PGSODIUM_LIBSODIUM_SYMBOLS_H'
  awk '{ print "#define " $1 " " $2 }' .pgsodium-private/redefine.syms
  echo '#endif'
} > .pgsodium-private/pgsodium-libsodium-symbols.h
LC_ALL=C nm -g --defined-only -P .pgsodium-private/libsodium-pgsodium.a | \
  awk '$1 ~ /^[A-Za-z_][A-Za-z0-9_]*$/ { print $1 }' | \
  awk '!/^%{private_prefix}/ { bad = 1; print > "/dev/stderr" } END { exit bad }'

%check
%{__make} check

%install
%{__rm} -rf %{buildroot}
install -d %{buildroot}%{private_includedir}
install -d %{buildroot}%{private_libdir}
cp -a src/libsodium/include/sodium %{buildroot}%{private_includedir}/
install -m 0644 src/libsodium/include/sodium.h \
  %{buildroot}%{private_includedir}/sodium.h
install -m 0644 .pgsodium-private/pgsodium-libsodium-symbols.h \
  %{buildroot}%{private_includedir}/
install -m 0644 .pgsodium-private/libsodium-pgsodium.a \
  %{buildroot}%{private_libdir}/

%files
%license LICENSE
%{private_includedir}/
%{private_libdir}/libsodium-pgsodium.a

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 1.0.22-1PGSTY
- Package a private symbol-prefixed PIC static libsodium for pgsodium
