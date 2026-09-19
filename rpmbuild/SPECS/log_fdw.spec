%global pname log_fdw
%global sname log_fdw
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
Version:	1.5
Release:	1PGSTY%{?dist}
Summary:	foreign-data wrapper for Postgres log file access
License:	Apache-2.0
URL:		https://github.com/aws/postgresql-logfdw
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This is a PostgreSQL extension built using Foreign-Data Wrapper facility to enable reading log files via SQL.
It basically provides SQL interface to create foreign tables for each PostgreSQL log file through which the file
contents can be read and analyzed. Only superusers are allowed to create this extension.

%prep
%setup -q -n postgresql-logfdw-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} USE_PGXS=1 install DESTDIR=%{buildroot}

%files
%license LICENSE NOTICE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 1.5-1PGSTY
- Update to 1.5
- Include the upstream license and notice in the binary package

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Add the complete LLVM toolchain and package its bitcode payload explicitly

* Fri Oct 31 2025 Vonng <rh@vonng.com> - 1.4-2PIGSTY
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.4-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
