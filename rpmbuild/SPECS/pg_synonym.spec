%global pname pg_synonym
%global sname pg_synonym
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_synonym only supports PostgreSQL 15 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.0
Release:        1PGSTY%{?dist}
Summary:        Automatically maintained table and view synonyms for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/Mazuco/pg_synonym
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/Mazuco/pg_synonym/archive/refs/tags/v1.0.0.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
pg_synonym provides synonyms backed by security-invoker views and event
triggers that keep them in sync with changes to their target relations.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 1.0.0-1PGSTY
- Initial RPM release for PostgreSQL 15 through 18
