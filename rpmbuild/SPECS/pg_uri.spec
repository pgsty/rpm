%global pname uri
%global sname pg_uri
%global rpmname pguri
%global oldname pg_uri_%{pgmajorversion}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_uri only supports PostgreSQL 14 through 18 in PGSTY builds}
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

Name:		%{rpmname}_%{pgmajorversion}
Version:	1.20251029
Release:	2PIGSTY%{?dist}
Summary:	URI Data type for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/petere/pguri
Source0:	pguri-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 uriparser-devel
Requires:	postgresql%{pgmajorversion}-server
Provides:	%{oldname} = %{version}-%{release}
Provides:	%{oldname}%{?_isa} = %{version}-%{release}
Obsoletes:	%{oldname} < %{version}-%{release}

%description
https://twitter.com/pvh/status/567395527357001728

This is an extension for PostgreSQL that provides a uri data type. Advantages over using plain text for storing URIs include:

URI syntax checking
functions for extracting URI components
human-friendly sorting
The actual URI parsing is provided by the uriparser library, which supports URI syntax as per RFC 3986.

Note that this might not be the right data type to use if you want to store user-provided URI data, such as HTTP referrers, since they might contain arbitrary junk.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{oldname}-llvmjit = %{version}-%{release}
Provides:	%{oldname}-llvmjit%{?_isa} = %{version}-%{release}
Obsoletes:	%{oldname}-llvmjit < %{version}-%{release}
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
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n pguri-%{version}

%build
PG_CPPFLAGS=-Wno-int-conversion PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

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
* Thu Jul 30 2026 Vonng <rh@vonng.com> - 1.20251029-2PIGSTY
- Align package name with PGDG and obsolete pg_uri_$v packages
- Limit PGSTY builds to PostgreSQL 14 through 18

* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.20251029-1PIGSTY
- https://github.com/petere/pguri/releases/tag/1.20251029
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.20151224
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
