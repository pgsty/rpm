%global sname pgq
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgq supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        3.5.2
Release:        1PGSTY%{?dist}
Summary:        Generic queue for PostgreSQL
License:        ISC
URL:            https://github.com/pgq/pgq
Source0:        pgq-3.5.2.tar.gz
# https://github.com/pgq/pgq/releases/tag/v3.5.2

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make python3
Requires:       postgresql%{pgmajorversion}-server

%{!?llvm:%global llvm 1}
%if %llvm
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

%description
PgQ provides transactional queueing and event processing in PostgreSQL.

%prep
%setup -q -n pgq-3.5.2

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}  %{with_llvm_arg}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make}  %{with_llvm_arg} install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE
%doc README.rst
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/contrib/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 3.5.2-1PGSTY
- Add the upstream 3.5.2 package for PostgreSQL 14 through 18
