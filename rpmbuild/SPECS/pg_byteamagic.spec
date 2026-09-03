%global pname pg_byteamagic
%global sname pg_byteamagic
%global extname byteamagic
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
Version:	0.2.4
Release:	1PGSTY%{?dist}
Summary:	Detect MIME types and file formats from PostgreSQL bytea values
License:	BSD-2-Clause
URL:		https://github.com/nmandery/pg_byteamagic
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/nmandery/pg_byteamagic/archive/refs/tags/v0.2.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
BuildRequires:	file-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_byteamagic exposes the libmagic database to PostgreSQL through the
byteamagic extension, allowing SQL queries to inspect a bytea value and
return either its MIME type or a human-readable file type description.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license COPYING
%doc README.md
%doc doc/byteamagic.md
%{pginstdir}/lib/%{extname}.so
%{pginstdir}/share/extension/%{extname}.control
%{pginstdir}/share/extension/%{extname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/byteamagic.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.2.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2.4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
