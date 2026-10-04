%global pname pg_textsearch
%global sname pg_textsearch
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_textsearch 1.5.1 only supports PostgreSQL 17 and 18}
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
Version:	1.5.1
Release:	1PGSTY%{?dist}
Summary:	BM25-based full-text search for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/timescale/pg_textsearch
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/timescale/pg_textsearch/releases/download/v1.5.1/pg_textsearch-1.5.1.tar.gz
#           Supported: PostgreSQL 17, 18 only

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc

%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_textsearch is a PostgreSQL extension providing BM25-based full-text search
functionality with relevance ranking. Developed by Timescale.

Features:
- Simple query syntax: ORDER BY content <@> 'search terms'
- Configurable BM25 parameters (k1, b)
- Support for multiple language configurations
- Partitioned table compatibility
- PostgreSQL 17 and 18 compatible

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 1.5.1-1PGSTY
- Update to 1.5.1.

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.4.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 1.4.0

* Thu May 14 2026 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
- https://github.com/timescale/pg_textsearch/releases/tag/v1.2.0
* Thu Apr 30 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- https://github.com/timescale/pg_textsearch/releases/tag/v1.1.0
* Mon Apr 06 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- https://github.com/timescale/pg_textsearch/releases/tag/v1.0.0
* Sat Feb 07 2026 Vonng <rh@vonng.com> - 0.5.0-1PIGSTY
- https://github.com/timescale/pg_textsearch/releases/tag/v0.5.0
* Sat Jan 17 2026 Vonng <rh@vonng.com> - 0.4.0-1PIGSTY
* Mon Dec 16 2024 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
