%global pname topn
%global sname topn
%global srcname postgresql-topn
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:topn supports PostgreSQL 14 through 18 in Pigsty}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.7.1
Release:        1PGSTY%{?dist}
Summary:        Approximate top-N aggregates for PostgreSQL
License:        AGPL-3.0-only
URL:            https://github.com/citusdata/postgresql-topn
Source0:        %{srcname}-%{version}.tar.gz
#               https://github.com/citusdata/postgresql-topn/archive/refs/tags/v2.7.1.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
TopN provides approximate top-value aggregation, incremental updates and
union operations using compact JSONB summaries.

%prep
%setup -q -n %{srcname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
    install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.7.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Initial Pigsty RPM package for TopN 2.7.1
- Include the JSONB memory-safety fixes from the v2.7.1 release
