%global pname pg_roast
%global sname pg_roast
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_commit ccbf012d01ebbb8edcb13b02add981705dab2308

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_roast supports PostgreSQL 14 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PIGSTY%{?dist}
Summary:        Opinionated PostgreSQL database auditor
License:        PostgreSQL
URL:            https://github.com/samirketema/pg_roast
Source0:        %{sname}-%{version}.tar.gz
#               upstream main snapshot ccbf012d01ebbb8edcb13b02add981705dab2308; no release tag is available

BuildRequires:  gcc make pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgresql%{pgmajorversion}-devel
Requires:       postgresql%{pgmajorversion}-server

%description
pg_roast audits schema design, security configuration, operational health,
and query behavior from inside PostgreSQL. Its background worker can run
periodic audits when pg_roast is added to shared_preload_libraries, while
manual audits remain available without preloading.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{snapshot_commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHECKS.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release from upstream snapshot ccbf012
- Build for PostgreSQL 14 through 18
