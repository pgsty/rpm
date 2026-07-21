%global pname online_advisor
%global sname online_advisor
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:online_advisor only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PIGSTY%{?dist}
Summary:        Suggest missing indexes and extended statistics online
License:        PostgreSQL
URL:            https://github.com/knizhnik/online_advisor
Source0:        %{sname}-%{version}.tar.gz
Patch0:         online_advisor-1.0.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
online_advisor instruments query execution and reports candidate indexes,
extended statistics, and statements that may benefit from being prepared.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides LLVM bitcode for %{sname}.
%endif

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

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
%{pginstdir}/lib/bitcode/%{pname}/*.bc
%endif

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release for upstream 1.0
