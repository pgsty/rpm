%global sname wal2mongo
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.7
Release:        1PIGSTY%{?dist}
Summary:        Logical decoding output plugin for MongoDB
License:        Apache-2.0
URL:            https://github.com/HighgoSoftware/%{sname}
Source0:        %{sname}-%{version}.tar.gz
Patch0:         wal2mongo-1.0.7-pg17.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
Requires:       postgresql%{pgmajorversion}-server

%description
wal2mongo is a logical decoding output plugin that formats PostgreSQL changes
as MongoDB commands.

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
%if 0%{?pgmajorversion} >= 17
%patch -P 0 -p1
%endif

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE NOTICE
%doc README.md README.cn.md
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*
%endif

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 1.0.7-1PIGSTY
- Initial RPM release with PostgreSQL 17 and 18 compatibility
