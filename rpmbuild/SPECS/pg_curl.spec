%global pname pg_curl
%global sname pg_curl
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global pg_curl_commit 6abdb3dbe81c0e320eebeeb0120cff993d593b31
%global whitelist_commit 9001c0cb09483e0828c2578f8e842cf00268a44e

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_curl supports PostgreSQL 14 through 18}
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
Version:	2.5.0
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL tool for transferring data with URL syntax
License:	MIT
URL:		https://github.com/RekGRpth/pg_curl
Source0:	%{sname}-%{version}.tar.gz
# Official PGXN 2.5.0 with the exact upstream pg_whitelist submodule.
# pg_curl %{pg_curl_commit} and pg_whitelist %{whitelist_commit}.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libcurl-devel
BuildRequires:	gcc
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	    postgresql%{pgmajorversion}-server

%description
PostgreSQL tool for transferring data with URL syntax, supporting DICT, FILE, FTP, FTPS, GOPHER, GOPHERS, HTTP, HTTPS, IMAP, IMAPS,
 LDAP,LDAPS, MQTT, POP3, POP3S, RTMP, RTMPS, RTSP, SCP, SFTP, SMB, SMBS, SMTP, SMTPS, TELNET, TFTP, WS and WSS.
This package combines the official PGXN source with pg_whitelist at
%{whitelist_commit}. The upstream SQL version is 2.5 and includes
the 2.4 to 2.5 catalog upgrade script.

%prep
%setup -q -n %{sname}-%{version}
grep -qx "default_version = '2.5'" %{pname}.control
test -s %{pname}--2.4.sql
test -s %{pname}--2.4--2.5.sql

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}


%files
%doc README.md
%doc SOURCE-MANIFEST.pgsty
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 07 2026 Ruohang Feng <rh@vonng.com> - 2.5.0-1PGSTY
- Update to the official PGXN 2.5.0 release.
- Include the pinned pg_whitelist submodule and upstream 2.4 to 2.5 upgrade script.
- Remove the obsolete downstream 2.4.1 SQL migration workaround.

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 2.4.6-1PGSTY
- Update to 2.4.6

* Tue Sep 01 2026 Vonng <rh@vonng.com> - 2.4.5-3.git20260815.f7a70f3PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Package the deterministic master-tag and pg_whitelist composite source
- Add downstream extension version 2.4.1 with an in-place 2.4 upgrade edge
- Preserve all previously published SQL scripts byte-for-byte

* Sun Oct 26 2025 Vonng <rh@vonng.com> - 2.4.5-2PIGSTY
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 2.4.5-1PIGSTY
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 2.4.2-1PIGSTY
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 2.4.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
