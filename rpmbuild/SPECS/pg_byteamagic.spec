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

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.4
Release:	1PIGSTY%{?dist}
Summary:	Detect MIME types and file formats from PostgreSQL bytea values
License:	BSD-2-Clause
URL:		https://github.com/nmandery/pg_byteamagic
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/nmandery/pg_byteamagic/archive/refs/tags/v0.2.4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
BuildRequires:	file-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_byteamagic exposes the libmagic database to PostgreSQL through the
byteamagic extension, allowing SQL queries to inspect a bytea value and
return either its MIME type or a human-readable file type description.

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
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license COPYING
%doc README.md
%doc doc/byteamagic.md
%{pginstdir}/lib/%{extname}.so
%{pginstdir}/share/extension/%{extname}.control
%{pginstdir}/share/extension/%{extname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/byteamagic.md

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2.4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
