%global sname pg_background
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.4
Release:	1PGSTY%{?dist}
Summary:	Execute SQL commands in PostgreSQL background worker processes
License:	PostgreSQL
URL:		https://github.com/vibhorkum/%{sname}
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_background-2.0.4.patch
#		https://github.com/vibhorkum/pg_background/archive/refs/tags/v2.0.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_background executes SQL commands in PostgreSQL background worker processes.
It supports asynchronous execution and autonomous transactions for long-running
operations without blocking client sessions.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 2.0.4-1PGSTY
- Update to 2.0.4.

* Tue Sep 01 2026 Vonng <rh@vonng.com> - 2.0.3-2PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
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
