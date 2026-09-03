%global pname roaringbitmap
%global sname pg_roaringbitmap
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
Version:	1.2.0
Release:	1PGSTY%{?dist}
Summary:	RoaringBitmap extension for PostgreSQL.
License:	Apache-2.0
URL:		https://github.com/ChenHuajun/pg_roaringbitmap
Source0:	pg_roaringbitmap-%{version}.tar.gz
#           https://github.com/ChenHuajun/pg_roaringbitmap/archive/refs/tags/v1.2.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
RoaringBitmap extension for PostgreSQL.
Roaring bitmaps are compressed bitmaps which tend to outperform conventional compressed bitmaps such as WAH, EWAH or Concise.
In some instances, roaring bitmaps can be hundreds of times faster and they often offer significantly better compression.
They can even be faster than uncompressed bitmaps. More information https://github.com/RoaringBitmap/CRoaring .

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Jul 01 2026 Vonng <rh@vonng.com> - 1.2.0-2PIGSTY
- Use system llvm-lto path for builder LLVM version compatibility

* Tue Jun 30 2026 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
- https://github.com/ChenHuajun/pg_roaringbitmap/releases/tag/v1.2.0
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- https://github.com/ChenHuajun/pg_roaringbitmap/releases/tag/v1.1.0
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.5.5-1PIGSTY
* Wed Sep 13 2023 Vonng <rh@vonng.com> - 0.5.4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
