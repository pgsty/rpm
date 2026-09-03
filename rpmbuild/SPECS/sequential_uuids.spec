%global pname sequential_uuids
%global sname sequential_uuids
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
Version:	1.0.3
Release:	1PGSTY%{?dist}
Summary:	generator of sequential UUIDs
License:	MIT
URL:		https://github.com/tvondra/sequential-uuids
Source0:	sequential-uuids-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements two UUID generators with sequential patterns,
which helps to reduce random I/O patterns associated with regular entirely-random UUID.

Regular random UUIDs are distributed uniformly over the whole range of possible values.
This results in poor locality when inserting data into indexes - all index leaf pages are
equally likely to be hit, forcing the whole index into memory. With small indexes that's fine,
but once the index size exceeds shared buffers (or RAM), the cache hit ratio quickly deteriorates.

%prep
%setup -q -n sequential-uuids-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Oct 26 2025 Vonng <rh@vonng.com> - 1.0.3-2PIGSTY
- with official pg18 support
* Thu Jan 09 2025 Vonng <rh@vonng.com> - 1.0.3-1PIGSTY
- with official pg16/17 support
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
