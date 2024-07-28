Name:           scws
Version:        1.2.3
Release:        1PIGSTY%{?dist}
Summary:        Simple Chinese Word Segmentation
License:        BSD
URL:            http://www.xunsearch.com/scws/
Source0:        http://www.xunsearch.com/scws/down/%{name}-%{version}.tar.bz2

BuildRequires:  gcc, make
Requires:       glibc

%description
SCWS (Simple Chinese Word Segmentation) is a high performance Chinese word segmentation utility.

%prep
%setup -q

%build
LDFLAGS="-Wl,--disable-new-dtags" ./configure
make

%install
make install DESTDIR=%{buildroot}

%files
/usr/local/bin/scws
/usr/local/bin/scws-gen-dict
/usr/local/lib/libscws.*
/usr/local/include/scws/*
/usr/local/etc/rules.ini
/usr/local/etc/rules.utf8.ini
/usr/local/etc/rules_cht.utf8.ini
%exclude /usr/lib/.build-id/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Wed Sep 13 2023 Vonng <rh@vonng.com> - 1.2.3-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>