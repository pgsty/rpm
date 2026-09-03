%global sname pg_incremental
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
Version:	1.5.0
Release:	1PGSTY%{?dist}
Summary:	Incremental Data Processing in PostgreSQL
License:	PostgreSQL
URL:		https://github.com/CrunchyData/pg_incremental
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/CrunchyData/pg_incremental/archive/refs/tags/v1.5.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_incremental is a simple extension that helps you do fast,
reliable, incremental batch processing in PostgreSQL.

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
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.5.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.5.0-1PIGSTY
- https://github.com/CrunchyData/pg_incremental/releases/tag/v1.5.0
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.4.1-1PIGSTY
- https://github.com/CrunchyData/pg_incremental/releases/tag/v1.4.1
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 1.2.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
