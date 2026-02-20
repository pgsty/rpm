%global sname antlr4-runtime413

Name:           %{sname}
Version:        4.13.2
Release:        1PIGSTY%{?dist}
Summary:        ANTLR4 C++ runtime library 4.13
License:        BSD-3-Clause
URL:            https://www.antlr.org/
Source0:        antlr4-cpp-runtime-%{version}-source.zip

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libuuid-devel
BuildRequires:  unzip

%description
ANTLR4 C++ runtime shared library used by Babelfish parser components.

%package devel
Summary:        Development files for ANTLR4 C++ runtime 4.13
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       antlr4-runtime-devel = %{version}-%{release}
Conflicts:      antlr4-runtime-devel

%description devel
Headers and development files for ANTLR4 C++ runtime 4.13.

%prep
%setup -q -c -T -n %{name}-%{version}
unzip -q %{SOURCE0}

%build
cmake -S . -B build \
  -DANTLR_BUILD_CPP_TESTS=OFF \
  -DANTLR_BUILD_STATIC=OFF \
  -DANTLR_BUILD_SHARED=ON \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_lib}
cmake --build build %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build
%{__rm} -f %{buildroot}%{_libdir}/libantlr4-runtime.a
%{__rm} -rf %{buildroot}%{_datadir}/doc/libantlr4

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc README.md
%{_libdir}/libantlr4-runtime.so.4*

%files devel
%{_includedir}/antlr4-runtime/*
%{_libdir}/libantlr4-runtime.so

%changelog
* Thu Feb 19 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 4.13.2-1PIGSTY
- Package ANTLR4 runtime as standalone runtime/devel RPMs for Babelfish
