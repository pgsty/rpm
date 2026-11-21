%global pname plx
%global sname plx
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %{!?llvm:%global llvm 1}
%else
 %{!?llvm:%global llvm 1}
%endif

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:plx 3.1.0 supports PostgreSQL 15 through 19 in PGSTY builds}
%endif

%if %llvm
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        3.1.0
Release:        1PGSTY%{?dist}
Summary:        Transpile multiple procedural dialects to PL/pgSQL
License:        MIT
URL:            https://github.com/commandprompt/plx
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/commandprompt/plx/archive/refs/tags/v3.1.0.tar.gz

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
Oracle PL/SQL, Transact-SQL, Lua, or C# syntax into PL/pgSQL at CREATE FUNCTION time.

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
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 3.1.0-1PGSTY
- Update to upstream 3.1.0, including the Lua and C# dialects.
- Install the upstream 2.0.0 to 3.0.0 to 3.1.0 SQL upgrade chain.

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.0.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 2.0.1
- Package extension SQL through version 2.0.0

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.3.1-1PIGSTY
- Initial RPM release for plx 1.3.1 and PostgreSQL 14 through 18
