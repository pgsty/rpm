Name:           scws
Version:        1.2.3
Release:        1PGSTY%{?dist}
Summary:        Simple Chinese Word Segmentation
License:        BSD-3-Clause
URL:            http://www.xunsearch.com/scws/
Source0:        scws-%{version}.tar.bz2
#               http://www.xunsearch.com/scws/down/scws-1.2.3.tar.bz2

BuildRequires:  gcc, make
Requires:       glibc

%description
SCWS (Simple Chinese Word Segmentation) is a high performance Chinese word segmentation utility.

%prep
%setup -q

%build
%set_build_flags
export LT_SYS_LIBRARY_PATH=%{_libdir}
%configure --disable-static --sysconfdir=%{_sysconfdir}/scws
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{_libdir}/libscws.la

%files
%{_bindir}/scws
%{_bindir}/scws-gen-dict
%{_libdir}/libscws.so*
%{_includedir}/scws/*
%{_sysconfdir}/scws/rules.ini
%{_sysconfdir}/scws/rules.utf8.ini
%{_sysconfdir}/scws/rules_cht.utf8.ini
%exclude /usr/lib/.build-id/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Sat Sep 05 2026 Vonng <rh@vonng.com> - 1.2.3-1PGSTY
- Use standard RPM paths and export the system library path to avoid invalid RPATHs

* Wed Sep 13 2023 Vonng <rh@vonng.com> - 1.2.3
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
