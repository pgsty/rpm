%global pname pg_accumulator
%global sname pg_accumulator
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14
%{error:pg_accumulator only supports PostgreSQL 14+}
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
Version:	1.1.3
Release:	1PIGSTY%{?dist}
Summary:	Accumulation registers for balance and turnover tracking in PostgreSQL
License:	PostgreSQL
URL:		https://github.com/Treedo/pg_accumulator
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_accumulator/1.1.3/pg_accumulator-1.1.3.zip
#           Supported: PostgreSQL 14+

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_accumulator provides declarative accumulation registers for PostgreSQL,
with transactional balance and turnover tracking across arbitrary dimensions.

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
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.MD docs/README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/%{pname}.md
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sat Apr 25 2026 Vonng <rh@vonng.com> - 1.1.3-1PIGSTY
- Initial RPM release for pg_accumulator 1.1.3 from PGXN
