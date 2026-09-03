%global pname re2
%global sname re2
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:re2 only supports PostgreSQL 16 through 18 in PGSTY builds}
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
Version:	0.4.1
Release:	1PGSTY%{?dist}
Summary:	ClickHouse-compatible regular expression functions powered by RE2
License:	PostgreSQL
URL:		https://github.com/ClickHouse/pg_re2
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/re2/0.4.1/re2-0.4.1.zip
#           Supported: PostgreSQL 16, 17, 18

BuildRequires:	gcc-c++
BuildRequires:	re2-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
re2 provides ClickHouse-compatible regular expression functions for PostgreSQL
16 and later, backed by Google's RE2 engine.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md doc/re2.md
%license LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.4.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 0.4.1-1PIGSTY
- Update to upstream PGXN 0.4.1

* Sun Jul 05 2026 Vonng <rh@vonng.com> - 0.4.0-1PIGSTY
- Update to upstream PGXN 0.4.0 using the normalized source tarball

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Update to upstream PGXN 0.3.0 using the normalized source tarball

* Fri Apr 17 2026 Vonng <rh@vonng.com> - 0.1.1-1PIGSTY
- Update to upstream 0.1.1 with the normalized PGXN source bundle

* Thu Apr 16 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release from the official PGXN 0.1.0 source bundle
