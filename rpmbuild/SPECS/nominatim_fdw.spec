%global pname nominatim_fdw
%global sname nominatim_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:nominatim_fdw only supports PostgreSQL 14 through 18 in PGSTY builds}
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
Version:	2.2.0
Release:	1PGSTY%{?dist}
Summary:	Nominatim Foreign Data Wrapper for PostgreSQL
License:	MIT
URL:		https://github.com/jimjonesbr/nominatim_fdw
Source0:	%{sname}-%{version}.tar.gz
Patch0:		nominatim_fdw-2.2.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libcurl-devel libxml2-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
nominatim_fdw is a PostgreSQL Foreign Data Wrapper (FDW) to access data from
Nominatim servers using simple function calls.

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE
%{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 2.2.0-1PGSTY
- Update to 2.2.0

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Jul 27 2026 Vonng <rh@vonng.com> - 2.1.0-1PIGSTY
- Update to upstream PGXN 2.1.0 and refresh the EL8 libcurl patch

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- Update to upstream PGXN 2.0.0
- Guard nghttp2 version reporting for the older EL8 libcurl API

* Fri Apr 10 2026 Vonng <rh@vonng.com> - 1.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
