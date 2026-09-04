%global pname pg_curl
%global sname pg_curl
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20260815
%global snapshot_commit f7a70f37d469e783d8268cb91af445145cbe005d
%global snapshot_short f7a70f3
%global whitelist_commit fbca6aef6962b20126714eaaa3f55c77f65bb5c3
%global source_version 2.4.5+git%{snapshot_date}.%{snapshot_short}

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
Version:	2.4.5
Release:	3.git%{snapshot_date}.%{snapshot_short}PGSTY%{?dist}
Summary:	PostgreSQL tool for transferring data with URL syntax
License:	MIT
URL:		https://github.com/RekGRpth/pg_curl
Source0:	%{sname}-%{source_version}.tar.gz
Patch0:		pg_curl-2.4.5+git20260815.f7a70f3.patch
# Deterministic composite of pg_curl f7a70f37d469e783d8268cb91af445145cbe005d
# and pg_whitelist fbca6aef6962b20126714eaaa3f55c77f65bb5c3.

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
This package uses snapshot %{snapshot_commit} with its exact pg_whitelist
gitlink filled from %{whitelist_commit}.

%prep
%setup -q -n %{sname}-%{source_version}
cp pg_curl--2.4.sql pg_curl--2.4.1.sql
patch -p1 --fuzz=0 < %{PATCH0}

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
