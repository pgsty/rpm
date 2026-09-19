%global sname pg_circuit
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_circuit supports PostgreSQL 16-18}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        Runtime protection against dangerous PostgreSQL statements
License:        Apache-2.0
URL:            https://github.com/PG-Circuit/pg-circuit
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pg_circuit-0.1.0-pg18.patch
# Official release tarball; the archive has no enclosing directory.

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
PG Circuit Community inspects SQL statements and can observe, warn or
block risky DML and DDL operations. Enable pg_circuit in
shared_preload_libraries and restart PostgreSQL before use.
Community reports runtime pressure but does not automatically change modes.

%prep
%setup -q -c -n pg_circuit-0.1.0
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} DOCS=

%install
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot} DOCS=

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/lib/%{sname}.so
%if %llvm
%{pginstdir}/lib/bitcode/%{sname}/
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Package upstream 0.1.0 for PostgreSQL 16 through 18
- Adapt timestamp includes and WAL counters for PostgreSQL 18
