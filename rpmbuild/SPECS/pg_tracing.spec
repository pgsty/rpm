%global pname pg_tracing
%global sname pg_tracing
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
Version:	0.1.3
Release:	1PGSTY%{?dist}
Summary:	Distributed Tracing for PostgreSQL
License:	MIT
URL:		https://github.com/DataDog/pg_tracing
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libcurl-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_tracing is a PostgreSQL extension that generates server-side spans for distributed tracing.
When pg_tracing is active, it generates spans on sampled queries. To access these spans, the extension provides two ways:

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}


%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Sep 05 2025 Vonng <rh@vonng.com> - 0.1.3-2PIGSTY
- pg18 support with https://github.com/DataDog/pg_tracing/commit/
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 0.1.3-1PIGSTY
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 0.1.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
