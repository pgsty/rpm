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

Name:		%{sname}_%{pgmajorversion}
Version:	2.0
Release:	1.git20260808.ff37a7c8PGSTY%{?dist}
Summary:	A PostgreSQL foreign data wrapper for Redis
License:	PostgreSQL
URL:		https://github.com/pg-redis-fdw/redis_fdw
Source0:	%{sname}-2.0+git20260808.ff37a7c8.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 hiredis-devel
%if %llvm
BuildRequires:	clang llvm
%endif
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for the Redis key/value database: http://redis.io/
This code was originally experimental, and largely intended as a pet project for Dave to experiment with and learn about FDWs in PostgreSQL. It has now been extended for production use by Andrew.
By all means use it, but do so entirely at your own risk! You have been warned!

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n redis_fdw-%{snapshot_commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_PGXS=1 install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.0-1.git20260808.ff37a7c8PGSTY
- Package upstream master snapshot ff37a7c82f3f
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 1.0-2PIGSTY
- add PG 18 support, merge into one source tarball
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
