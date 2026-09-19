%global pname psql_bm25s
%global sname psql_bm25s
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:psql_bm25s supports PostgreSQL 17-18}
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
Version:	0.4.14
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension for BM25-family lexical retrieval
License:	Apache-2.0
URL:		https://github.com/Intelligent-Internet/psql_bm25s
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/Intelligent-Internet/psql_bm25s/releases/tag/v0.4.14
#           Supported upstream CI/release matrix: PostgreSQL 17, 18

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc libicu-devel pkgconf-pkg-config
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
psql_bm25s is an independent PostgreSQL extension for BM25-family lexical
retrieval. It implements a PostgreSQL-native access method with BM25 ranking,
tokenization helpers, mutable-workload index maintenance, and SQL query
interfaces.

%prep
%setup -q -n II-42-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}

%files
%doc README.md docs/*.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.4.14-1PGSTY
- Update to 0.4.14

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.4.13-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu May 14 2026 Vonng <rh@vonng.com> - 0.4.13-1PIGSTY
- Package upstream release v0.4.13 for PostgreSQL 17-18
