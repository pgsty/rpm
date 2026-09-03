%global pname pg_roast
%global sname pg_roast
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_commit ccbf012d01ebbb8edcb13b02add981705dab2308

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_roast supports PostgreSQL 14 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PGSTY%{?dist}
Summary:        Opinionated PostgreSQL database auditor
License:        PostgreSQL
URL:            https://github.com/samirketema/pg_roast
Source0:        %{sname}-%{version}.tar.gz
#               upstream main snapshot ccbf012d01ebbb8edcb13b02add981705dab2308; no release tag is available

BuildRequires:  gcc make pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pg_roast audits schema design, security configuration, operational health,
and query behavior from inside PostgreSQL. Its background worker can run
periodic audits when pg_roast is added to shared_preload_libraries, while
manual audits remain available without preloading.

%prep
%setup -q -n %{sname}-%{snapshot_commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHECKS.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release from upstream snapshot ccbf012
- Build for PostgreSQL 14 through 18
