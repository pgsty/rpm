%global pname pg_rusage
%global sname pg_rusage
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_rusage only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PGSTY%{?dist}
Summary:        Backend CPU and resource usage measurements for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/michaelpq/pg_plugins
Source0:        pg_plugins-ae57c1f3df69.tar.gz
# Source: https://codeload.github.com/michaelpq/pg_plugins/tar.gz/ae57c1f3df697fb942f4576f873a655187193ace
# SHA256: 8e977f51901e1cb5357a24d16b7385aff58da7883c606eff195fc2923c8d5c15

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Backend CPU and resource usage measurements for PostgreSQL.

%prep
%setup -q -n pg_plugins-ae57c1f3df697fb942f4576f873a655187193ace

%build
PATH=%{pginstdir}/bin:$PATH %{__make} -C pg_rusage %{with_llvm_arg}  %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} -C pg_rusage %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md pg_rusage/README
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.0-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
