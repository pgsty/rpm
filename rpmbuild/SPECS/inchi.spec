%define debug_package %{nil}
%global sname inchi

Name:           %{sname}
Version:        1.07.3
Release:        1PIGSTY%{?dist}
Summary:        IUPAC International Chemical Identifier shared library
License:        MIT
URL:            https://github.com/IUPAC-InChI/InChI
Source0:        %{sname}-%{version}.tar.gz
# normalized from the official upstream release archive:
# https://github.com/IUPAC-InChI/InChI/releases/download/v1.07.3/INCHI-1-SRC.zip

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
%setup -q -n %{sname}-%{version}

%build
%{__mkdir_p} build
make -C INCHI_API/demos/inchi_main/gcc \
  CREATE_MAIN= \
  LIB_DIR=%{_builddir}/%{sname}-%{version}/build \
  INCHI_LIB_NAME=libinchi \
  C_COMPILER="%{__cc}" \
  C_SO_OPTIONS="-fPIC -DTARGET_API_LIB -DCOMPILE_ANSI_ONLY" \
  C_OPTIONS="%{optflags} -std=c11 -c -fno-strict-aliasing"

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_libdir}
install -m 0755 build/libinchi.so.1.07 %{buildroot}%{_libdir}/libinchi.so.1.07
ln -sf libinchi.so.1.07 %{buildroot}%{_libdir}/libinchi.so

%{__mkdir_p} %{buildroot}%{_includedir}/inchi
install -m 0644 INCHI_BASE/src/inchi_api.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI_BASE/src/bcf_s.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI_BASE/src/ichi.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI_BASE/src/ixa.h %{buildroot}%{_includedir}/inchi/
install -m 0644 INCHI_BASE/src/inchicmp.h %{buildroot}%{_includedir}/inchi/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc readme.txt
%{_libdir}/libinchi.so.1.07

%files devel
%{_includedir}/inchi/bcf_s.h
%{_includedir}/inchi/inchi_api.h
%{_includedir}/inchi/ichi.h
%{_includedir}/inchi/ixa.h
%{_includedir}/inchi/inchicmp.h
%{_libdir}/libinchi.so

%changelog
* Mon Apr 13 2026 Vonng <rh@vonng.com> - 1.07.3-1PIGSTY
- Package InChI 1.07.3 as standalone runtime and devel RPMs for EL10
- Install the shared library and headers in the locations expected by RDKit
- Include bcf_s.h in the devel payload for RDKit's InChI adapter build
