%global pname pg_auth_mon
%global sname pg_auth_mon
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_auth_mon 5.0 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        5.0
Release:        1PGSTY%{?dist}
Summary:        Monitor PostgreSQL authentication attempts per role
License:        MIT
URL:            https://github.com/RafiaSabih/pg_auth_mon
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/RafiaSabih/pg_auth_mon/archive/refs/tags/v5.0.tar.gz

BuildRequires:  gcc
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_auth_mon records successful and failed PostgreSQL authentication attempts
per role. The module must be added to shared_preload_libraries and PostgreSQL
must be restarted before the extension is created.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides LLVM bitcode for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config \
    %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config \
    install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 5.0-1PGSTY
- Initial Pigsty RPM package for pg_auth_mon 5.0
- Package extension version 1.1 and require shared preloading
