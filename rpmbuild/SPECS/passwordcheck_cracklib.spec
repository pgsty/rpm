%global pname passwordcheck_cracklib
%global sname passwordcheck_cracklib
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:passwordcheck_cracklib 3.2.0 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        3.2.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL password checks backed by CrackLib
License:        LGPL-2.1-only
URL:            https://github.com/devrimgunduz/passwordcheck_cracklib
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/devrimgunduz/passwordcheck_cracklib/archive/refs/tags/3.2.0.tar.gz

BuildRequires:  gcc
BuildRequires:  cracklib-devel
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server
Requires:       cracklib-dicts

%description
passwordcheck_cracklib rejects weak PostgreSQL role passwords using CrackLib.
It is a module-only package with no CREATE EXTENSION objects. Add the module to
shared_preload_libraries and restart PostgreSQL to enable it for all sessions.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} \
    PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} \
    PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 3.2.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Initial Pigsty RPM package for passwordcheck_cracklib 3.2.0
- Keep the Enterprise Linux CrackLib dictionary path and require its data
