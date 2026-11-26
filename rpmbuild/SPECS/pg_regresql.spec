%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:pg_regresql is packaged for PostgreSQL 15 through 19}
%endif

%global pname pg_regresql
%global sname pg_regresql
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
Version:	2.2.1
Release:	1PGSTY%{?dist}
Summary:	Trust pg_class statistics for query planning instead of physical file size
License:	BSD-2-Clause AND PostgreSQL
URL:		https://github.com/boringsql/regresql
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_regresql is a PostgreSQL extension that forces the planner to use pg_class
statistics instead of estimates from physical file size.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} enable_rpath=no %{with_llvm_arg} %{?_smp_mflags} all

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} enable_rpath=no %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE restore/README.md
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Nov 24 2026 Ruohang Feng <rh@vonng.com> - 2.2.1-1PGSTY
- Use the upstream PostgreSQL 19 planner hook.

* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 2.2.0-1PGSTY
- Update to upstream 2.2.0 with extended-statistics restore backports.
- Drop the default-goal patch now included upstream and record PostgreSQL licensing.
- Keep PostgreSQL 19 excluded pending a replacement for get_relation_info_hook.

* Wed Oct 21 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PGSTY
- Update to upstream 2.1.0.
- Include the default build target patch in the source RPM.

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.0.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Restore automatic debuginfo and debugsource generation with %setup

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
