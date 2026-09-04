%global pname redis_fdw
%global sname redis_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_commit ff37a7c82f3f10d5478e56082733f2af87e69380

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0
Release:	1.git20260808.ff37a7c8PGSTY%{?dist}
Summary:	A PostgreSQL foreign data wrapper for Redis
License:	PostgreSQL
URL:		https://github.com/pg-redis-fdw/redis_fdw
Source0:	%{sname}-2.0+git20260808.ff37a7c8.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 hiredis-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for the Redis key/value database: http://redis.io/
This code was originally experimental, and largely intended as a pet project for Dave to experiment with and learn about FDWs in PostgreSQL. It has now been extended for production use by Andrew.
By all means use it, but do so entirely at your own risk! You have been warned!

%prep
%setup -q -n redis_fdw-%{snapshot_commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} USE_PGXS=1 install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.0-1.git20260808.ff37a7c8PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Package upstream master snapshot ff37a7c82f3f
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 1.0-2PIGSTY
- add PG 18 support, merge into one source tarball
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
