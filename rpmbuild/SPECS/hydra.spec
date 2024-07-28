%define debug_package %{nil}
%global pname columnar
%global sname hydra
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
Version:	1.1.2
Release:	1PIGSTY%{?dist}
Summary:	Hydra: Column-oriented Postgres. Add scalable analytics to your project in minutes.
License:	Apache-2.0
URL:		https://github.com/hydradatabase/%{sname}
Source0:	https://github.com/hydradatabase/hydra/archive/refs/tags/hydra-1.1.2.tar.gz
#           https://github.com/hydradatabase/hydra/archive/refs/tags/v1.1.1.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Hydra is open source, column-oriented Postgres.
You can query billions of rows instantly on Postgres without code changes.
Parallelized analytics in minutes, not weeks.

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
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif


%prep
%setup -q -n %{sname}-%{version}

%build
cd columnar
./configure
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
cd columnar
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/include/server/citus_version.h
%exclude /usr/lib/.build-id/*
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 1.1.2
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 1.1.1
* Thu Jan 11 2024 Vonng <rh@vonng.com> - 1.1.0
* Sat Sep 23 2023 Vonng <rh@vonng.com> - 1.0.0
- Initial RPM release, used by Pigsty <https://pigsty.io>