%global sname pg_background
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.9.2
Release:	1PIGSTY%{?dist}
Summary:	Execute SQL commands in PostgreSQL background worker processes
License:	PostgreSQL
URL:		https://github.com/vibhorkum/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#		https://github.com/vibhorkum/pg_background/archive/refs/tags/v1.9.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
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

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

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
* Fri Apr 10 2026 Vonng <rh@vonng.com> - 1.9.2-1PIGSTY
- Initial RPM release
- https://github.com/vibhorkum/pg_background/releases/tag/v1.9.2
