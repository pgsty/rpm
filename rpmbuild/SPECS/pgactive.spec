%global pname pgactive
%global sname pgactive
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.5
Release:	1PIGSTY%{?dist}
Summary:	Active-active Replication Extension for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/aws/pgactive
SOURCE0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
pgactive is a PostgreSQL replication extension for creating an active-active database.

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
BuildRequires:  llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{pname}-%{version}

%build
./configure
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 2.1.5-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>