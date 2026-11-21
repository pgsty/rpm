%global pname pg_similarity
%global sname pg_similarity
%global pginstdir /usr/pgsql-%{pgmajorversion}

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
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1PGSTY%{?dist}
Summary:	Functions and operators for executing similarity queries
License:	BSD-3-Clause
URL:		https://github.com/eulerto/pg_similarity
Source0:	pg_similarity-%{version}.tar.gz
Patch0:        pg_similarity-1.0-pg19-uint8.patch
#           https://github.com/eulerto/pg_similarity/archive/refs/tags/pg_similarity_1_0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_similarity is an extension to support similarity queries on PostgreSQL.
The implementation is tightly integrated in the RDBMS in the sense that it
defines operators so instead of the traditional operators (= and <>)
you can use ~~~ and ! (any of these operators represents a similarity function).

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 1.0-1PGSTY
- Add PostgreSQL 19 header and type compatibility.

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Jul 22 2024 Vonng <rh@vonng.com> - 1.0
- patch for PostgreSQL 16
* Mon Oct 16 2023 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
