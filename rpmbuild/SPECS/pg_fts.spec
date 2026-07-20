%define debug_package %{nil}
%global pname pg_fts
%global sname pg_fts
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_fts 0.2.0 only supports PostgreSQL 17 and 18}
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
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	Full-text search with BM25 ranking for PostgreSQL
License:	PostgreSQL AND MIT
URL:		https://codeberg.org/gregburd/pg_fts
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_fts/0.2.0/pg_fts-0.2.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc clang llvm
Requires:	postgresql%{pgmajorversion}-server

%description
pg_fts provides BM25 and BM25F relevance ranking, a dedicated inverted-index
access method, and boolean, phrase, NEAR, prefix, fuzzy, and regex queries.

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
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

%files
%license LICENSE
%doc README.md CHANGELOG.md CAPABILITIES.md ROADMAP.md doc/MIGRATING_FROM_PG_TEXTSEARCH.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Mon Jul 20 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.2.0
- Package PostgreSQL 17 and 18 builds with LLVM bitcode subpackages
