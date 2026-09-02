%global sname pg_background
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.3
Release:	2PGSTY%{?dist}
Summary:	Execute SQL commands in PostgreSQL background worker processes
License:	PostgreSQL
URL:		https://github.com/vibhorkum/%{sname}
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_background-2.0.3.patch
#		https://github.com/vibhorkum/pg_background/archive/refs/tags/v2.0.3.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	clang >= 19.0
BuildRequires:	llvm >= 19.0
%endif
Requires:	postgresql%{pgmajorversion}-server

%description
pg_background executes SQL commands in PostgreSQL background worker processes.
It supports asynchronous execution and autonomous transactions for long-running
operations without blocking client sessions.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 2.0.3-2PGSTY
- Add downstream extension version 2.0.3 and a 2.0 to 2.0.3 security upgrade edge
- Preserve every previously published 2.0 install and upgrade script byte-for-byte
- Declare the Clang and LLVM toolchain required by the llvmjit build

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.0.3-1PIGSTY
- Update to upstream 2.0.3 with search-path, catalog, cancellation, worker lifecycle, and result safety fixes

* Fri Jun 19 2026 Vonng <rh@vonng.com> - 2.0.2-1PIGSTY
- https://github.com/vibhorkum/pg_background/releases/tag/v2.0.2

* Sat Jun 06 2026 Vonng <rh@vonng.com> - 2.0-1PIGSTY
- https://github.com/vibhorkum/pg_background/releases/tag/v2.0

* Fri Apr 10 2026 Vonng <rh@vonng.com> - 1.9.2-1PIGSTY
- Initial RPM release
- https://github.com/vibhorkum/pg_background/releases/tag/v1.9.2
