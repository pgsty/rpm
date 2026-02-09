%global sname pg_incremental
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

Name:		%{sname}_%{pgmajorversion}
Version:	1.4.1
Release:	1PIGSTY%{?dist}
Summary:	Incremental Data Processing in PostgreSQL
License:	PostgreSQL
URL:		https://github.com/CrunchyData/pg_incremental
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/CrunchyData/pg_incremental/archive/refs/tags/v1.4.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_incremental is a simple extension that helps you do fast,
reliable, incremental batch processing in PostgreSQL.


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
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif


%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.4.1-1PIGSTY
- https://github.com/CrunchyData/pg_incremental/releases/tag/v1.4.1
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 1.2.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
