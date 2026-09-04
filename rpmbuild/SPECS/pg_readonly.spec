%global pname pg_readonly
%global sname pg_readonly
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_readonly supports PostgreSQL 14 through 18 in Pigsty}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.6
Release:        1PGSTY%{?dist}
Summary:        Set all PostgreSQL cluster databases read only
License:        PostgreSQL
URL:            https://github.com/pierreforstmann/pg_readonly
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/pierreforstmann/pg_readonly/archive/refs/tags/1.0.6.tar.gz
Patch0:         pg_readonly-1.0.6.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pg_readonly provides a cluster-wide in-memory read-only switch and rejects
write statements while the switch is enabled.

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
    install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.0.6-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Initial Pigsty RPM package for pg_readonly 1.0.6
- Add downstream metadata-only 1.0.5 to 1.0.6 transition
