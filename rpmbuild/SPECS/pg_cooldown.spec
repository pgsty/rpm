%global pname pg_cooldown
%global sname pg_cooldown
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
Version:	0.1
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension to remove buffered pages for specific relations.
License:	Apache-2.0
URL:		https://github.com/rbergm/pg_cooldown
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libcurl-devel

%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	libcurl

%description
PostgreSQL extension to remove all pages of specific relations from the shared buffer.
The extension was heavily inspired by pg_prewarm and functions as a complementary tool: Whereas pg_prewarm adds pages from a relation to the shared buffer, pg_cooldown removes them again.
The main purpose of this tool is to easily simulate cold-start scenarios in research.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1  %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}


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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Feb 10 2025 Vonng <rh@vonng.com> - 0.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
