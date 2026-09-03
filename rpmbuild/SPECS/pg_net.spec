%global pname pg_net
%global sname pg_net
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?rhel} >= 10
%global pg_net_version 0.20.5
%else
%global pg_net_version 0.9.2
%endif

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
Version:	%{pg_net_version}
Release:	1PGSTY%{?dist}
Summary:	A PostgreSQL extension that enables asynchronous (non-blocking) HTTP/HTTPS requests with SQL
License:	Apache-2.0
URL:		https://github.com/supabase/pg_net
Source0:	pg_net-%{version}.tar.gz
#           Upstream release archive uses the matching v-prefixed tag.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if 0%{?rhel} >= 10
BuildRequires:	libcurl-devel >= 7.83
%else
BuildRequires:	libcurl-devel
%endif
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	    postgresql%{pgmajorversion}-server

%description
The PG_NET extension enables PostgreSQL to make asynchronous HTTP/HTTPS requests in SQL.
It eliminates the need for servers to continuously poll for database changes and instead allows the database to proactively notify external resources about significant events.
 It seamlessly integrates with triggers, cron jobs (e.g., PG_CRON), and procedures, unlocking numerous possibilities.
 Notably, PG_NET powers Supabase's Webhook functionality, highlighting its robustness and reliability.

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
%if 0%{?rhel} >= 10
%{pginstdir}/include/server/extension/%{pname}/
%endif
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.20.5-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Jul 28 2026 Vonng <rh@vonng.com> - 0.20.5-3PIGSTY
- Use pg_net 0.9.2 with the system libcurl on EL8 and EL9
- Keep pg_net 0.20.5 on EL10 where libcurl 7.83 or newer is available

* Thu Jul 23 2026 Vonng <rh@vonng.com> - 0.20.5-1PIGSTY
- https://github.com/supabase/pg_net/releases/tag/v0.20.5
* Sat Jun 06 2026 Vonng <rh@vonng.com> - 0.20.3-1PIGSTY
- https://github.com/supabase/pg_net/releases/tag/v0.20.3
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 0.20.2-1PIGSTY
- https://github.com/supabase/pg_net/releases/tag/v0.20.2
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.20.0-1PIGSTY
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.9.2-1PIGSTY
* Thu May 09 2024 Vonng <rh@vonng.com> - 0.9.1-1PIGSTY
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 0.8.0-1PIGSTY
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 0.7.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
