%global pname pg_describe
%global sname pg_describe
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_describe only supports PostgreSQL 17 and 18}
%endif

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.0
Release:        1PGSTY%{?dist}
Summary:        Describe query parameters and result columns without execution
License:        MIT
URL:            https://github.com/sajonaro/pg_describe
Source0:        %{sname}-%{version}.tar.gz
#               normalized from https://api.pgxn.org/dist/pg_describe/1.0.0/pg_describe-1.0.0.zip

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc
Requires:       postgresql%{pgmajorversion}-server

%description
pg_describe reports the parameters and result columns of a SQL query without
executing it. It exposes type, name, provenance, and nullability information
through a PostgreSQL function.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} \
  PG_CONFIG=%{pginstdir}/bin/pg_config LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} \
  PG_CONFIG=%{pginstdir}/bin/pg_config LLVM_BINPATH=%{llvm_binpath}

%files
%license LICENSE
%doc README.md docs
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Aug 07 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.0
- Package the upstream-supported PostgreSQL 17 and 18 releases
