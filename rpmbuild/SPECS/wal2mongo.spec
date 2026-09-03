%global sname wal2mongo
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.7
Release:        1PGSTY%{?dist}
Summary:        Logical decoding output plugin for MongoDB
License:        Apache-2.0
URL:            https://github.com/HighgoSoftware/%{sname}
Source0:        %{sname}-%{version}.tar.gz
Patch0:         wal2mongo-1.0.7.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
wal2mongo is a logical decoding output plugin that formats PostgreSQL changes
as MongoDB commands.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?pgmajorversion} >= 17
%patch -P 0 -p1
%endif

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE NOTICE
%doc README.md README.cn.md
%{pginstdir}/lib/%{sname}.so

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.7-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Jul 22 2026 Vonng <rh@vonng.com> - 1.0.7-1PIGSTY
- Initial RPM release with PostgreSQL 17 and 18 compatibility
