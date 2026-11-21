%global sname plr
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:plr supports PostgreSQL 15 through 19 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        8.4.8.11
Release:        1PGSTY%{?dist}
Summary:        R procedural language for PostgreSQL
License:        GPL-2.0-or-later
URL:            https://github.com/postgres-plr/plr
Source0:        plr-8.4.8.11.tar.gz
# https://github.com/postgres-plr/plr/releases/tag/REL8_4_8_11

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make R-devel pkgconfig
Requires:       postgresql%{pgmajorversion}-server

%{!?llvm:%global llvm 1}
%if %llvm
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

%description
PL/R allows PostgreSQL functions to execute R code.

%prep
%setup -q -n plr-REL8_4_8_11

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_PGXS=1 %{with_llvm_arg}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{with_llvm_arg} install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 8.4.8.11-1PGSTY
- Update to upstream 8.4.8.11.

* Thu Nov 05 2026 Vonng <rh@vonng.com> - 8.4.8.10-1PGSTY
- Add the upstream 8.4.8.10 package for PostgreSQL 14 through 18
