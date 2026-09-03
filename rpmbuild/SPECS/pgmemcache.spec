%global sname pgmemcache
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	A PostgreSQL API to interface with memcached
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.0
Release:	1PGSTY%{?dist}
License:	MIT
Source0:	%{sname}-%{version}.tar.gz
URL:		https://github.com/Ohmu/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libmemcached-devel
BuildRequires:	pgdg-srpm-macros cyrus-sasl-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server libmemcached

Obsoletes:	%{sname}-%{pgmajorversion} < 2.3.0-4

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
	install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%doc README.rst
%license LICENSE
%{pginstdir}/lib/pgmemcache.so
%{pginstdir}/share/extension/pgmemcache--*.sql
%{pginstdir}/share/extension/pgmemcache.control

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%{pginstdir}/lib/bitcode/%{sname}/
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.3.0-1PGSTY
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Align LLVM dependencies and move PGXS bitcode into llvmjit

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 2.3.0-5PIGSTY
- Rebuild EL8 aarch64 packages for PostgreSQL 14 and 15

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-5
- Update package metadata
