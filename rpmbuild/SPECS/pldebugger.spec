%global sname pldebugger
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pldebugger supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.10
Release:        1PGSTY%{?dist}
Summary:        Server-side debugger for PL/pgSQL
License:        Artistic-2.0
URL:            https://github.com/EnterpriseDB/pldebugger
Source0:        pldebugger-1.10.tar.gz
# https://github.com/EnterpriseDB/pldebugger/releases/tag/v1.10

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make
Requires:       postgresql%{pgmajorversion}-server

%{!?llvm:%global llvm 1}
%if %llvm
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

%description
The PL/pgSQL debugger API supports debugging functions with clients such as pgAdmin.

%prep
%setup -q -n pldebugger-1.10

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_PGXS=1 %{with_llvm_arg}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{with_llvm_arg} install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license README-pldebugger.md
%doc README-pldebugger.md
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 1.10-1PGSTY
- Add the upstream 1.10 package for PostgreSQL 14 through 18
