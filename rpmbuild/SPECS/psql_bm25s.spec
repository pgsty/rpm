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

Name:		%{sname}_%{pgmajorversion}
Version:	0.4.13
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension for BM25-family lexical retrieval
License:	Apache-2.0
URL:		https://github.com/Intelligent-Internet/psql_bm25s
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/Intelligent-Internet/psql_bm25s/releases/tag/v0.4.13
#           Supported upstream CI/release matrix: PostgreSQL 17, 18

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc libicu-devel pkgconf-pkg-config
Requires:	postgresql%{pgmajorversion}-server

%description
psql_bm25s is an independent PostgreSQL extension for BM25-family lexical
retrieval. It implements a PostgreSQL-native access method with BM25 ranking,
tokenization helpers, mutable-workload index maintenance, and SQL query
interfaces.

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
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}

%files
%doc README.md docs/*.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Thu May 14 2026 Vonng <rh@vonng.com> - 0.4.13-1PIGSTY
- Package upstream release v0.4.13 for PostgreSQL 17-18
