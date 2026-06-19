%global pname pg_ducklake
%global sname pg_ducklake
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
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	DuckLake lakehouse extension for PostgreSQL
License:	MIT
URL:		https://github.com/relytcloud/pg_ducklake
Source0:	%{sname}-%{version}.tar.gz
Patch0:		patches/%{sname}-%{version}-rpm-tarball-build.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc gcc-c++ make cmake ninja-build patch pkgconf-pkg-config
BuildRequires:	bison flex zlib-devel readline-devel libxml2-devel libxslt-devel
BuildRequires:	openssl-devel libcurl-devel lz4-devel CRoaring-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_ducklake is a PostgreSQL extension for managed DuckLake tables, backed by
DuckDB and Parquet files. It requires shared_preload_libraries = 'pg_ducklake'
before CREATE EXTENSION.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
PATH=%{pginstdir}/bin:$PATH PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} install DESTDIR=%{buildroot}

%files
%doc README.md pg_ducklake/docs
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/lib/bitcode/*
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for pg_ducklake 1.0.0
