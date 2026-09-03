%global pname pg_snakeoil
%global sname pg_snakeoil
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
Version:	1.4
Release:	1PGSTY%{?dist}
Summary:	The PostgreSQL Antivirus
License:	PostgreSQL
URL:		https://github.com/credativ/pg_snakeoil
Source0:	pg_snakeoil-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 clamav-devel >= 0.100.0
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Running typical on-access antivirus software on a PostgreSQL server has severe drawbacks such as severely affecting performance or making the filesystem unreliable. The failure modes are extremely problematic when a non-PostgreSQL-aware scanner blocks access to a file due to viruses, or even false-positives and bugs in the scanner software.
We typically recommend not to run such software on PostgreSQL servers, as PostgreSQL knows how to discern between code and data and will not execute any viruses stored in a database. However, running anti-virus software is sometimes required by local policy.
pg_snakeoil provides ClamAV scanning of all data in PostgreSQL in a way that does not interfere with the proper functioning of PostgreSQL and does not cause collateral damage or unnecessary downtimes.

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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Mar 20 2025 Vonng <rh@vonng.com> - 1.4
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.3
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
