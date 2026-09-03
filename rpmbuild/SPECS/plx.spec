%global pname plx
%global sname plx
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %{!?llvm:%global llvm 1}
%else
 %{!?llvm:%global llvm 1}
%endif

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:plx 2.0.1 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.0.1
Release:        1PGSTY%{?dist}
Summary:        Transpile multiple procedural dialects to PL/pgSQL
License:        MIT
URL:            https://github.com/commandprompt/plx
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/commandprompt/plx/archive/refs/tags/v2.0.1.tar.gz

BuildRequires:  gcc
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
plx is a dialect-pluggable procedural language extension. It transpiles
functions written in Ruby, PHP, JavaScript, TypeScript, Python, Go, COBOL,
Oracle PL/SQL, or Transact-SQL syntax into PL/pgSQL at CREATE FUNCTION time.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} PG_CONFIG=%{pginstdir}/bin/pg_config \
    %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.0.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 2.0.1
- Package extension SQL through version 2.0.0

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.3.1-1PIGSTY
- Initial RPM release for plx 1.3.1 and PostgreSQL 14 through 18
