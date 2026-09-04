%global pname http
%global sname pgsql_http
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
Version:	1.7.2
Release:	1PGSTY%{?dist}
Summary:	HTTP client for PostgreSQL, retrieve a web page from inside the database.
License:	MIT
URL:		https://github.com/pramsey/pgsql-http
Source0:	pgsql-http-%{version}.tar.gz
#           https://github.com/pramsey/pgsql-http/archive/refs/tags/v1.7.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 libcurl-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Provides:	pg_http_%{pgmajorversion} = %{version}-%{release}
Obsoletes:	pg_http_%{pgmajorversion} < %{version}-%{release}

%description
Wouldn't it be nice to be able to write a trigger that called a web service? Either to get back a result,
 or to poke that service into refreshing itself against the new state of the database? This extension is for that.

%prep
%setup -q -n pgsql-http-%{version}

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
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.7.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 1.7.2

* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.7.1-1PIGSTY
- Update to 1.7.1
* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.7.0-1PIGSTY
- Rename RPM package name to pgsql_http
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.7.0
- Rename package name to pg_http
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 1.6.3
- Rename package name to pg_http
* Mon Dec 16 2024 Vonng <rh@vonng.com> - 1.6.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
* Wed Sep 13 2023 Vonng <rh@vonng.com> - 1.6.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
