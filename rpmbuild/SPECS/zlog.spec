Name:           zlog
Version:        1.2.18
Release:        1PIGSTY%{?dist}
Summary:        High-performance C logging library
License:        Apache-2.0
URL:            https://github.com/HardySimpson/zlog
Source0:        zlog-%{version}.tar.gz
%define debug_package %{nil}

BuildRequires:  gcc, make

%description
zlog is a reliable, high-performance, thread-safe logging library for C.
This package ships the zlog header and static/shared libraries needed by
PolarDB-FileSystem.

%prep
%setup -q -n zlog-%{version}

%build
%{__make} %{?_smp_mflags}

%install
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -m 0644 src/zlog.h %{buildroot}%{_includedir}/
install -m 0644 src/libzlog.a %{buildroot}%{_libdir}/
install -m 0755 src/libzlog.so.1.2 %{buildroot}%{_libdir}/
ln -s libzlog.so.1.2 %{buildroot}%{_libdir}/libzlog.so.1
ln -s libzlog.so.1.2 %{buildroot}%{_libdir}/libzlog.so

%files
%license LICENSE
%doc README.md Changelog
%{_includedir}/zlog.h
%{_libdir}/libzlog.a
%{_libdir}/libzlog.so
%{_libdir}/libzlog.so.1
%{_libdir}/libzlog.so.1.2

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.2.18-1PIGSTY
- Initial Pigsty package for zlog
