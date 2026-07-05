%global pname re2
%global sname re2
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

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

Name:		%{sname}_%{pgmajorversion}
Version:	0.4.0
Release:	1PIGSTY%{?dist}
Summary:	ClickHouse-compatible regular expression functions powered by RE2
License:	PostgreSQL
URL:		https://github.com/ClickHouse/pg_re2
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/re2/0.4.0/re2-0.4.0.zip
#           Supported: PostgreSQL 16, 17, 18

BuildRequires:	gcc-c++
BuildRequires:	re2-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
re2 provides ClickHouse-compatible regular expression functions for PostgreSQL
16 and later, backed by Google's RE2 engine.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
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
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

%files
%doc README.md doc/re2.md
%license LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sun Jul 05 2026 Vonng <rh@vonng.com> - 0.4.0-1PIGSTY
- Update to upstream PGXN 0.4.0 using the normalized source tarball

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Update to upstream PGXN 0.3.0 using the normalized source tarball

* Fri Apr 17 2026 Vonng <rh@vonng.com> - 0.1.1-1PIGSTY
- Update to upstream 0.1.1 with the normalized PGXN source bundle

* Thu Apr 16 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release from the official PGXN 0.1.0 source bundle
