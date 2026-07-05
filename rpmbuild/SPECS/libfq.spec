%global pname libfq

Name:		libfq
Version:	0.6.2
Release:	1PIGSTY%{?dist}
Summary:	A wrapper library for the Firebird C API, loosely based on libpq

License:	PostgreSQL
URL:		https://github.com/ibarwick/libfq
Source0:	%{pname}-%{version}.tar.gz

BuildRequires:	firebird-devel >= 2.0.0
BuildRequires:	gcc make
%if 0%{?rhel} && 0%{?rhel} >= 8
Requires:	libfbclient2
%else
Requires:	firebird-libfbclient
%endif

%description
A wrapper library for the Firebird C API, loosely based on PostgreSQL's libpq.
It provides a number of functions which act as convenience wrappers around the
native Firebird C API. Function names begin with FQ rather than PQ, with
more-or-less identical signatures, plus some Firebird-specific functions.
This library is required by the firebird_fdw PostgreSQL foreign data wrapper.

%prep
%setup -q -n %{pname}-%{version}

%build
./configure --prefix=%{_prefix} --with-ibase=/usr/include/firebird --libdir=%{_libdir}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# drop useless libtool archive (EL10 strips it automatically, EL8/EL9 do not)
%{__rm} -f %{buildroot}%{_libdir}/libfq.la

%files
%{_libdir}/libfq.a
%{_libdir}/libfq.so
%{_libdir}/libfq-%{version}.so
%{_includedir}/libfq.h
%{_includedir}/libfq-expbuffer.h
%{_includedir}/libfq-version.h

%changelog
* Sun Jul 05 2026 Vonng <rh@vonng.com> - 0.6.2-1PIGSTY
- Add libfq 0.6.2 for the Pigsty RPM repository
- https://github.com/ibarwick/libfq/releases/tag/0.6.2
