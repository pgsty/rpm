%global sname pgmemcache
%global pginstdir /usr/pgsql-%{pgmajorversion}

Summary:	A PostgreSQL API to interface with memcached
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.0
Release:	5PIGSTY%{?dist}
License:	BSD
Source0:	%{sname}-%{version}.tar.gz
URL:		https://github.com/Ohmu/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libmemcached-devel
BuildRequires:	pgdg-srpm-macros cyrus-sasl-devel
Requires:	postgresql%{pgmajorversion}-server libmemcached

Obsoletes:	%{sname}-%{pgmajorversion} < 2.3.0-4

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} \
	install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%doc README.rst
%license LICENSE
%{pginstdir}/lib/pgmemcache.so
%{pginstdir}/share/extension/pgmemcache--*.sql
%{pginstdir}/share/extension/pgmemcache.control
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 2.3.0-5PIGSTY
- Rebuild EL8 aarch64 packages for PostgreSQL 14 and 15

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-5
- Update package metadata
