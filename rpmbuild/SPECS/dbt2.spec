%global debug_package %{nil}
%global _vpath_builddir .
%global sname dbt2
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Summary:	Database Test 2 Differences from the TPC-C - Extensions
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	0.61.7
Release:	1PIGSTY%{?dist}
License:	GPLv2+
Source0:	%{sname}-%{version}.tar.gz
Patch0:		dbt2-cmakelists-rpm.patch
URL:		https://github.com/osdldbt/%{sname}/
Requires:	%{sname}-common

BuildRequires:	gcc-c++
BuildRequires:	cmake >= 3.2.0
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libpq5-devel openssl-devel curl-devel expat-devel
%if 0%{?rhel} == 8
BuildRequires:	libev-devel
%endif

%description
The Open Source Development Lab's Database Test 2 (DBT-2) test kit.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for dbt2-extensions
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0

%description llvmjit
This package provides JIT support for dbt2-extensions.
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
CFLAGS="$CFLAGS -I%{pginstdir}/include/server -g -fPIE"; export CFLAGS
export PATH=%{pginstdir}/bin/:$PATH
%{__install} -d build
pushd build
%cmake ..
popd
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build
pushd storedproc/pgsql/c
%{__make} DESTDIR=%{buildroot}
popd

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin/:$PATH
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install DESTDIR=%{buildroot}
popd
pushd storedproc/pgsql/c
%{__make} DESTDIR=%{buildroot} install
popd
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/extension
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/lib
%{__cp} storedproc/pgsql/c/%{sname}.control %{buildroot}/%{pginstdir}/share/extension
%{__cp} storedproc/pgsql/c/%{sname}.so %{buildroot}/%{pginstdir}/lib
%{__cp} storedproc/pgsql/c/%{sname}--0.45.0.sql \
	%{buildroot}/%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{__rm} -f %{buildroot}/%{_bindir}/*
%{__rm} -f %{buildroot}/%{_mandir}/man1/dbt2*
%{__rm} -rf %{buildroot}/usr/src/%{sname}/storedproc/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/stock_level.sql
%{pginstdir}/share/delivery.sql
%{pginstdir}/share/new_order.sql
%{pginstdir}/share/order_status.sql
%{pginstdir}/share/payment.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 0.61.7-1PIGSTY
- Add libev development dependency for EL8 builds

* Thu Jul 10 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-1PGDG
- Update 0.61.7
