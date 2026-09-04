%global pname imgsmlr
%global sname imgsmlr
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20180223
%global snapshot_commit c484a15cc4ad254b0cc6cd7dc4820ad6472fcfac
%global snapshot_short c484a15

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
Version:	1.0
Release:	2.git%{snapshot_date}.%{snapshot_short}PGSTY%{?dist}
Summary:	PostgreSQL extension which implements similar images searching functionality.
License:	PostgreSQL
URL:		https://github.com/postgrespro/imgsmlr
Source0:	%{sname}-%{version}+git%{snapshot_date}.%{snapshot_short}.tar.gz
Patch0:		imgsmlr-1.0.patch
#           https://github.com/postgrespro/imgsmlr/archive/refs/heads/master.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 gd-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
ImgSmlr method is based on Haar wavelet transform.
The goal of ImgSmlr is not to provide most advanced state of art similar images searching methods.
ImgSmlr was written as sample extension which illustrate how PostgreSQL
extendability could cover such untypical tasks for RDBMS as similar images search.

%prep
%setup -q -n %{sname}-%{version}+git%{snapshot_date}.%{snapshot_short}
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
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.0-2.git20180223.c484a15PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Pin the clean upstream master snapshot c484a15
- Preserve PostgreSQL 14-18 and varlena compatibility in the local patch
- Declare clang and llvm for PGXS bitcode generation

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.0-2PIGSTY
- Fix varlena detoasting with newer toolchains

* Mon Jul 22 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
