%global pname plx
%global sname plx
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %{!?llvm:%global llvm 1}
%else
 %{!?llvm:%global llvm 1}
%endif

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:plx 1.3.1 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.3.1
Release:        1PIGSTY%{?dist}
Summary:        Transpile multiple procedural dialects to PL/pgSQL
License:        MIT
URL:            https://github.com/commandprompt/plx
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/commandprompt/plx/archive/refs/tags/v1.3.1.tar.gz

BuildRequires:  gcc
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
plx is a dialect-pluggable procedural language extension. It transpiles
functions written in Ruby, PHP, JavaScript, TypeScript, Python, Go, COBOL,
Oracle PL/SQL, or Transact-SQL syntax into PL/pgSQL at CREATE FUNCTION time.

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
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config \
    %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.3.1-1PIGSTY
- Initial RPM release for plx 1.3.1 and PostgreSQL 14 through 18
