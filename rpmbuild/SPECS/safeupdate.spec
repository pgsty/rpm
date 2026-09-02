%global pname safeupdate
%global sname safeupdate
%global srcname pg-safeupdate
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:safeupdate supports PostgreSQL 14 through 18 in Pigsty}
%endif

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        1.7
Release:        1PGSTY%{?dist}
Summary:        Require a WHERE clause for PostgreSQL UPDATE and DELETE
License:        ISC
URL:            https://github.com/eradman/pg-safeupdate
Source0:        %{srcname}-%{version}.tar.gz
#               https://github.com/eradman/pg-safeupdate/archive/refs/tags/1.7.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
safeupdate is a preloadable PostgreSQL module that rejects UPDATE and DELETE
statements without qualifying criteria. It has no CREATE EXTENSION objects.

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
%setup -q -n %{srcname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} \
    install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md NEWS
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.7-1PGSTY
- Initial Pigsty RPM package for safeupdate 1.7
- Preserve hook chaining and pg_upgrade compatibility fixes
