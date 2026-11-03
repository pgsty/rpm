Name:           zlog
Version:        1.2.20
Release:        1PGSTY%{?dist}
Summary:        High-performance C logging library
License:        Apache-2.0
URL:            https://github.com/HardySimpson/zlog
Source0:        zlog-%{version}.tar.gz

BuildRequires:  gcc, make

%description
zlog is a reliable, high-performance, thread-safe logging library for C.
This package ships the zlog header and static/shared libraries needed by
PolarDB-FileSystem.

%prep
%setup -q -n zlog-%{version}
%if 0%{?rhel} == 8
# GNU make 4.2 treats an unescaped hash in the version shell expression as a comment.
sed -i '/^ZLOG_VERSION :=/s/#define/\\#define/' src/Makefile
%endif

%build
%set_build_flags
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
* Tue Nov 03 2026 Vonng <rh@vonng.com> - 1.2.20-1PGSTY
- Update to 1.2.20 for the PolarStore and PolarDB rebuild.
- Apply distribution compiler and linker flags.
- Escape the version parser hash for GNU make 4.2 on EL8.

* Sun Aug 09 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.2.18-2PGSTY
- Rebuild with the PGSTY package release brand

* Mon Jul 06 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.2.18-1PIGSTY
- Initial Pigsty package for zlog
