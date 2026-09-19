%global pname pg_local_cache
%global sname pg_local_cache
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_local_cache only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

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
Version:	2.0.4
Release:	1PGSTY%{?dist}
Summary:	Transaction-aware cache for PostgreSQL primary-key reads
License:	MIT
URL:		https://github.com/profundium/pg_local_cache
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_local_cache-2.0.4.patch
#           official v2.0.4 source archive

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_local_cache keeps bounded whole-row entries in PostgreSQL shared memory and
accelerates supported primary-key reads while preserving PostgreSQL as the
source of truth. It targets one configured database and one writable primary.
The module must be added to shared_preload_libraries and PostgreSQL restarted
before its cache workers and SQL fast path can be used.

%prep
%setup -q -n %{sname}-%{version}-source
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 2.0.4-1PGSTY
- Update to 2.0.4

* Tue Sep 01 2026 Vonng <rh@vonng.com> - 2.0.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Upgrade to pg_local_cache 2.0.1
- Retain the 1.x get API with C compatibility entry points and catalog identity

* Wed Aug 12 2026 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
- Add RPM package for upstream PGXN 1.3.0 and PostgreSQL 14 through 18
- Document the shared_preload_libraries and single-primary requirements
