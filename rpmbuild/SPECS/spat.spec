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

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0a5
Release:	1.git%{gitdate}.%{shortcommit}PGSTY%{?dist}
Summary:	Redis-like In-Memory DB Embedded in Postgres
License:	AGPL-3.0-only
URL:		https://github.com/Florents-Tselai/spat
Source0:	%{sname}-%{version}+git%{gitdate}.%{shortcommit}.tar.gz
Patch0:		spat-0.1.0a5.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
spat is a Redis-like in-memory data structure server embedded in Postgres. Data is stored in Postgres shared memory.
The data model is key-value. Keys are strings, but values can be strings, lists, sets, or hashes.
This is stil in alpha and not production ready! Read notes on ACID below.

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
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%autosetup -p1 -n %{sname}-%{commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/include/server/extension/spat/spat.h
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.1.0a5-1.git20250512.fccb581PGSTY
- Update to upstream commit fccb581 (0.1.0a5)
- Add downstream metadata-only 0.1.0a4 to 0.1.0a5 transition

* Fri May 23 2025 Vonng <rh@vonng.com> - 0.1.0a4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
