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

Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:	1PIGSTY%{?dist}
Summary:	Transaction-aware cache for PostgreSQL primary-key reads
License:	MIT
URL:		https://github.com/profundium/pg_local_cache
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_local_cache/1.3.0/pg_local_cache-1.3.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_local_cache keeps bounded whole-row entries in PostgreSQL shared memory and
accelerates supported primary-key reads while preserving PostgreSQL as the
source of truth. It targets one configured database and one writable primary.
The module must be added to shared_preload_libraries and PostgreSQL restarted
before its cache workers and SQL fast path can be used.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Wed Aug 12 2026 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
- Add RPM package for upstream PGXN 1.3.0 and PostgreSQL 14 through 18
- Document the shared_preload_libraries and single-primary requirements
