%global pname spat
%global sname spat
%global commit fccb581ff3fd537a9df0114098e3e22d2d5fa465
%global gitdate 20250512
%global shortcommit fccb581
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 17
%{error:spat 0.1.0a5 supports PostgreSQL 17 only}
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
Version:	0.1.0a5
Release:	1.git%{gitdate}.%{shortcommit}PGSTY%{?dist}
Summary:	Redis-like In-Memory DB Embedded in Postgres
License:	AGPL-3.0-only
URL:		https://github.com/Florents-Tselai/spat
Source0:	%{sname}-%{version}+git%{gitdate}.%{shortcommit}.tar.gz
Patch0:		spat-0.1.0a5.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
spat is a Redis-like in-memory data structure server embedded in Postgres. Data is stored in Postgres shared memory.
The data model is key-value. Keys are strings, but values can be strings, lists, sets, or hashes.
This is stil in alpha and not production ready! Read notes on ACID below.

%prep
%autosetup -p1 -n %{sname}-%{commit}

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
%{pginstdir}/include/server/extension/spat/spat.h

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.1.0a5-1.git20250512.fccb581PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Update to upstream commit fccb581 (0.1.0a5)
- Add downstream metadata-only 0.1.0a4 to 0.1.0a5 transition

* Fri May 23 2025 Vonng <rh@vonng.com> - 0.1.0a4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
