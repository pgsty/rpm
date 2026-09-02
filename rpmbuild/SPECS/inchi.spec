%define debug_package %{nil}
%global sname inchi

Name:           %{sname}
Version:        1.07.5
Release:        1PGSTY%{?dist}
Summary:        IUPAC International Chemical Identifier shared library
License:        MIT
URL:            https://github.com/IUPAC-InChI/InChI
Source0:        %{sname}_%{version}+dfsg.orig.tar.xz
# Repacked reproducibly from the official v1.07.5 tag with the same
# Files-Excluded policy as the matching Debian source package.

BuildRequires:  gcc
BuildRequires:  make

%description
InChI is the IUPAC International Chemical Identifier reference implementation.
This package provides the shared library required by RDKit when InChI support is
enabled on EL10.

%package devel
Summary:        Development files for the InChI library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and link-time symlink for building software against the InChI shared
library.

%prep
%setup -q -n InChI-%{version}

%build
%{__mkdir_p} build
make -C INCHI-1-SRC/INCHI_API/demos/inchi_main/gcc \
  CREATE_MAIN= \
  LIB_DIR=%{_builddir}/InChI-%{version}/build \
  INCHI_LIB_NAME=libinchi \
  MAIN_VERSION=.1 \
  VERSION=.1.07 \
  C_COMPILER="%{__cc}" \
  C_SO_OPTIONS="-fPIC -DTARGET_API_LIB -DCOMPILE_ANSI_ONLY" \
  C_OPTIONS="%{optflags} -std=c11 -c -fno-strict-aliasing"

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_libdir}
install -m 0755 build/libinchi.so.1.07 %{buildroot}%{_libdir}/libinchi.so.1.07
ln -sf libinchi.so.1.07 %{buildroot}%{_libdir}/libinchi.so

%{__mkdir_p} %{buildroot}%{_includedir}/inchi
install -m 0644 INCHI-1-SRC/INCHI_BASE/src/inchi_api.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI-1-SRC/INCHI_BASE/src/bcf_s.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI-1-SRC/INCHI_BASE/src/ichi.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI-1-SRC/INCHI_BASE/src/ixa.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI-1-SRC/INCHI_BASE/src/inchicmp.h %{buildroot}%{_includedir}/inchi/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_libdir}/libinchi.so.1.07

%files devel
%{_includedir}/inchi/bcf_s.h
%{_includedir}/inchi/inchi_api.h
%{_includedir}/inchi/ichi.h
%{_includedir}/inchi/ixa.h
%{_includedir}/inchi/inchicmp.h
%{_libdir}/libinchi.so

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.07.5-1PGSTY
- Update to InChI 1.07.5 using the shared DFSG-repacked source archive
- Keep the libinchi 1.07 ABI and RDKit-facing development header layout

* Mon Apr 13 2026 Vonng <rh@vonng.com> - 1.07.3-1PIGSTY
- Package InChI 1.07.3 as standalone runtime and devel RPMs for EL10
- Install the shared library and headers in the locations expected by RDKit
- Include bcf_s.h in the devel payload for RDKit's InChI adapter build
