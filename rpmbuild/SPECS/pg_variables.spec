%if 0%{?pgmajorversion} > 18
%{error:PostgreSQL 19 is not enabled for this recipe; see the PG19 audit record}
%endif

%global pname pg_variables
%global sname pg_variables
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

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
Version:	1.2.5
Release:	2PGSTY%{?dist}
Summary:	Session variables with various types for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/postgrespro/pg_variables
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_variables-1.2.5.patch
Patch1:		pg_variables-1.2.5-composite-datum.patch
#		https://github.com/postgrespro/pg_variables/archive/refs/tags/v1.2.5.tar.gz

# New composite datum symbols require the November 2026 security minors.
%if 0%{?pgmajorversion} == 19
%global pg_min_version 19.0
%endif
%if 0%{?pgmajorversion} == 18
%global pg_min_version 18.7
%endif
%if 0%{?pgmajorversion} == 17
%global pg_min_version 17.12
%endif
%if 0%{?pgmajorversion} == 16
%global pg_min_version 16.16
%endif
%if 0%{?pgmajorversion} == 15
%global pg_min_version 15.20
%endif
%if 0%{?pgmajorversion} < 15
%{error:unsupported PostgreSQL major version}
%endif

BuildRequires:	postgresql%{pgmajorversion}-devel >= %{pg_min_version} pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server >= %{pg_min_version}

%description
The pg_variables module provides functions to work with session-scoped
variables of various types. Variables can be grouped into packages and can
optionally participate in transaction semantics.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}
patch -p1 --fuzz=0 < %{PATCH1}


%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} LLVM_BINPATH=%{llvm_binpath} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} LLVM_BINPATH=%{llvm_binpath} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Vonng <rh@vonng.com> - 1.2.5-2PGSTY
- Keep PostgreSQL 19 disabled after regression review; omit the unaccepted patch.
- Use PostgreSQL version conditionals supported by EL8 RPM.

* Thu Nov 19 2026 Ruohang Feng <rh@vonng.com> - 1.2.5-2PGSTY
- Preserve composite datum versions when copying stored records.
- Use the installed LLVM tool directory for PGXS bitcode indexing.
- Require PostgreSQL security minors providing the composite datum API.

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.5-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Apr 06 2026 Vonng <rh@vonng.com> - 1.2.5-1PIGSTY
- Initial RPM release
- Backport upstream fixes afdef5405e9de88eb4548ea0f6a9150add44c749 and
  33a38b172e8e5ec0590cc690300299fbc65f0d48
