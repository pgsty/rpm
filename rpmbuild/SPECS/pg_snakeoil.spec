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

Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	1PIGSTY%{?dist}
Summary:	The PostgreSQL Antivirus
License:	PostgreSQL
URL:		https://github.com/credativ/pg_snakeoil
Source0:	pg_snakeoil-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 clamav-devel >= 0.100.0
Requires:	postgresql%{pgmajorversion}-server

%description
Running typical on-access antivirus software on a PostgreSQL server has severe drawbacks such as severely affecting performance or making the filesystem unreliable. The failure modes are extremely problematic when a non-PostgreSQL-aware scanner blocks access to a file due to viruses, or even false-positives and bugs in the scanner software.
We typically recommend not to run such software on PostgreSQL servers, as PostgreSQL knows how to discern between code and data and will not execute any viruses stored in a database. However, running anti-virus software is sometimes required by local policy.
pg_snakeoil provides ClamAV scanning of all data in PostgreSQL in a way that does not interfere with the proper functioning of PostgreSQL and does not cause collateral damage or unnecessary downtimes.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.3
- Initial RPM release, used by Pigsty <https://pigsty.io>