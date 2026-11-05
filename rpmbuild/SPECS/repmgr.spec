%global sname repmgr
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:repmgr supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        5.5.1
Release:        1PGSTY%{?dist}
Summary:        Replication management tools for PostgreSQL
License:        GPL-3.0-or-later
URL:            https://github.com/EnterpriseDB/repmgr
Source0:        repmgr-5.5.1.tar.gz
# https://github.com/EnterpriseDB/repmgr/releases/tag/v5.5.1

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make libcurl-devel json-c-devel flex
BuildRequires:  libselinux-devel libxslt-devel pam-devel numactl-devel
Requires:       postgresql%{pgmajorversion}-server

%{!?llvm:%global llvm 1}
%if %llvm
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

%description
repmgr provides tools for managing PostgreSQL replication and failover.

%prep
%setup -q -n repmgr-5.5.1

%build
PG_CONFIG=%{pginstdir}/bin/pg_config PATH=%{pginstdir}/bin:$PATH ./configure
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}  %{with_llvm_arg}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make}  %{with_llvm_arg} install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE COPYRIGHT
%doc README.md
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql
%{pginstdir}/bin/repmgr*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 5.5.1-1PGSTY
- Add the upstream 5.5.1 package for PostgreSQL 14 through 18
