%global pname columnar
%global sname hydra
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
Version:	1.1.2
Release:	1PGSTY%{?dist}
Summary:	Hydra: Column-oriented Postgres. Add scalable analytics to your project in minutes.
License:	AGPL-3.0-only AND MIT AND PostgreSQL
URL:		https://github.com/hydradatabase/columnar
Source0:	hydra-%{version}.tar.gz
#           https://github.com/hydradatabase/hydra/archive/refs/tags/v1.1.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Hydra is open source, column-oriented Postgres.
You can query billions of rows instantly on Postgres without code changes.
Parallelized analytics in minutes, not weeks.

%prep
%setup -q -n %{sname}-%{version}

%build
%set_build_flags
cd columnar
./configure
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
cd columnar
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE columnar/LICENSE columnar/NOTICE columnar/vendor/safestringlib/LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/include/server/citus_version.h
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.1.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Apr 27 2024 Vonng <rh@vonng.com> - 1.1.2
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 1.1.1
* Thu Jan 11 2024 Vonng <rh@vonng.com> - 1.1.0
* Sat Sep 23 2023 Vonng <rh@vonng.com> - 1.0.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
