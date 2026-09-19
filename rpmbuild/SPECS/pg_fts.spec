%global pname pg_fts
%global sname pg_fts
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_fts 1.8.3 only supports PostgreSQL 17 and 18}
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
Version:	1.8.3
Release:	1PGSTY%{?dist}
Summary:	Full-text search with BM25 ranking for PostgreSQL
License:	PostgreSQL AND MIT
URL:		https://codeberg.org/gregburd/pg_fts
Source0:	%{sname}-%{version}.tar.gz
#           https://codeberg.org/gregburd/pg_fts/archive/v1.8.3.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_fts provides BM25 and BM25F relevance ranking, a dedicated inverted-index
access method, and boolean, phrase, NEAR, prefix, fuzzy, and regex queries.

%prep
%setup -q -n %{sname}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md ROADMAP.md doc/MIGRATING_FROM_PG_TEXTSEARCH.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 1.8.3-1PGSTY
- Update to 1.8.3

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.5.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 1.5.3
- Use the official Codeberg archive root

* Mon Jul 20 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.2.0
- Package PostgreSQL 17 and 18 builds with LLVM bitcode subpackages
