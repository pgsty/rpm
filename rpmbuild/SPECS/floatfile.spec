%global pname floatfile
%global sname floatfile
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
Version:	1.3.1
Release:	1PGSTY%{?dist}
Summary:	A Postgres extension to store float arrays in individual files
License:	MIT
URL:		https://github.com/pjungwir/floatfile
Source0:	floatfile-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
A Postgres extension to store float arrays in individual files, providing very fast querying
(especially when combined with aggs_for_arrays, aggs_for_vecs, or floatvec) without paying a huge cost to keep updating them.
The idea is that if you have 1 million FLOATs, it is much faster if you can load them as a single 8 MB chunk rather than
pulling from a million different places on disk. Sometimes you can just store your data as an array in a regular Postgres table,
but updating those arrays will be slow and cause painful MVCC churn. Since this extension keeps the data in a separate file,
appends are very fast and outside the MVCC system.

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
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.3.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Jan 10 2025 Vonng <rh@vonng.com> - 1.3.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
