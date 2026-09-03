%global pname bzip
%global sname pg_bzip
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
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PGSTY%{?dist}
Summary:	Bzip compression and decompression for Postgres
License:	MIT
URL:		https://github.com/steve-chavez/pg_bzip
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/steve-chavez/pg_bzip/archive/refs/tags/v1.0.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  bzip2-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
If you get data compressed as bzip2, whether through HTTP or from a file, it's convenient to decompress it in SQL.
pg_bzip does that, it provides functions to decompress and compress data using bzip2.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Feb 21 2025 Vonng <rh@vonng.com> - 1.0.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
