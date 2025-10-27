%global pname age
%global sname apache-age
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.5.0
Release:	2PIGSTY%{?dist}
Summary:	Graph Processing & Analytics for Relational Databases for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/apache/age
Source0:	%{pname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 perl-FindBin
Requires:	postgresql%{pgmajorversion}-server

%description
Apache AGE is an extension for PostgreSQL that enables users to leverage a graph database on top of the existing relational databases.
AGE is an acronym for A Graph Extension and is inspired by Bitnine's AgensGraph, a multi-model database fork of PostgreSQL.
The basic principle of the project is to create a single storage that handles both the relational and graph data model
so that the users can use the standard ANSI SQL along with openCypher, one of the most popular graph query languages today.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif


%prep
%setup -q -n %{pname}-%{version}

git checkout PG%{pgmajorversion}/v%{version}-rc0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 1.5.0-2PIGSTY
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 1.5.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>