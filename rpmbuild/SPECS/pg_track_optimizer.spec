%global pname pg_track_optimizer
%global sname pg_track_optimizer
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
Version:	0.9.2
Release:	1PGSTY%{?dist}
Summary:	Track planning decisions in comparison with execution reality
License:	MIT
URL:		https://github.com/danolivo/pg_track_optimizer
Source0:	pg_track_optimizer-%{version}.tar.gz
#           https://github.com/danolivo/pg_track_optimizer/archive/refs/tags/v0.9.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
A lightweight PostgreSQL extension for detecting suboptimal query plans by
analysing the gap between planner estimates and actual execution statistics.
It hooks into the executor to compare estimated rows vs actual rows for each
plan node, computing multiple error metrics using logarithmic scale. It tracks
queries in shared memory and surfaces the worst offenders to help DBAs identify
queries suffering from poor cardinality estimates.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.9.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Mar 21 2026 Vonng <rh@vonng.com> - 0.9.2-1PIGSTY
* Thu Feb 12 2026 Vonng <rh@vonng.com> - 0.9.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
