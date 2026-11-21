%global sname repmgr
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:repmgr supports PostgreSQL 15 through 19 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        5.5.1
Release:        1PGSTY%{?dist}
Summary:        Replication management tools for PostgreSQL
License:        GPL-3.0-or-later
URL:            https://github.com/EnterpriseDB/repmgr
Source0:        repmgr-5.5.1.tar.gz
Patch0:        repmgr-5.5.1-pg19-c11.patch
# https://github.com/EnterpriseDB/repmgr/releases/tag/v5.5.1

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make libcurl-devel json-c-devel flex
BuildRequires:  libselinux-devel libxslt-devel pam-devel numactl-devel
Requires:       postgresql%{pgmajorversion}-server

%{!?llvm:%global llvm 1}
%if %llvm
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

# PGDG split frontend archives out of -devel starting with PostgreSQL 19.
%if 0%{?pgmajorversion} >= 19
BuildRequires: postgresql%{pgmajorversion}-static
%endif

%description
repmgr provides tools for managing PostgreSQL replication and failover.

%prep
%setup -q -n repmgr-5.5.1
%patch -P 0 -p1

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
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 5.5.1-1PGSTY
- Add PostgreSQL 19 compilation compatibility.

* Thu Nov 05 2026 Vonng <rh@vonng.com> - 5.5.1-1PGSTY
- Add the upstream 5.5.1 package for PostgreSQL 14 through 18
