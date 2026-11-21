%global pname aggs_for_vecs
%global sname aggs_for_vecs
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
Version:	1.4.1
Release:	1PGSTY%{?dist}
Summary:	Postgres C extension with aggregate functions for array inputs
License:	MIT
URL:		https://github.com/pjungwir/aggs_for_vecs
Source0:	%{sname}-%{version}.tar.gz
Patch0:         aggs_for_vecs-1.4.1-pg19-numeric.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This is a C-based Postgres extension offering various aggregate functions like
min, max, avg, and var_samp that operate on arrays instead of scalars.
It treats each array as a "vector" and handles each element independently.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

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
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 1.4.1-1PGSTY
- Adapt numeric arithmetic to the PostgreSQL 19 ErrorSaveContext API.
- Use the installed LLVM tool directory for PGXS bitcode indexing.

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.4.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Mar 04 2026 Vonng <rh@vonng.com> - 1.4.1-1PIGSTY
- https://pgxn.org/dist/aggs_for_vecs/1.4.1/
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 1.4.0
* Wed Dec 11 2024 Vonng <rh@vonng.com> - 1.3.2
* Tue Oct 29 2024 Vonng <rh@vonng.com> - 1.3.1
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.3.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
