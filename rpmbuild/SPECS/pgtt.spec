%global pname pgtt
%global sname pgtt
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgtt supports PostgreSQL 14 through 18 in Pigsty}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        4.6
Release:        2PGSTY%{?dist}
Summary:        Oracle-style global temporary tables for PostgreSQL
License:        ISC
URL:            https://github.com/darold/pgtt
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/darold/pgtt/archive/refs/tags/v4.6.tar.gz
Patch0:         pgtt-4.6.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pgtt implements Oracle-style global temporary tables using persistent
templates and per-session temporary storage.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
    install DESTDIR=%{buildroot}

%files
%license COPYING
%doc README.md ChangeLog AUTHORS CONTRIBUTORS
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}-repair-public-acl.sql
%{pginstdir}/doc/extension/%{pname}.md
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 4.6-2PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Repair PUBLIC write ACLs on every registered pre-4.6 GTT template
- Preserve owners and named-role grants and ship an idempotent repair script
- Harden standard and CREATE TABLE AS template creation against default ACLs

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 4.6-1PIGSTY
- Initial Pigsty RPM package for pgtt 4.6
- Include trigger, ownership, SQL-injection and grant hardening fixes
