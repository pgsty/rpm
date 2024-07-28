%global pname tle
%global sname pg_tle
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
Version:	1.4.0
Release:	1PIGSTY%{?dist}
Summary:	Trusted Language Extensions for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/aws/%{sname}
Source0:	https://github.com/aws/%{sname}/archive/refs/tags/pg_tle-1.4.0.tar.gz
#           https://github.com/aws/pg_tle/archive/refs/tags/v1.4.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Trusted Language Extensions (TLE) for PostgreSQL (pg_tle) is an open source project that lets developers
extend and deploy new PostgreSQL functionality with lower administrative and technical overhead.
Developers can use Trusted Language Extensions for PostgreSQL to create and install extensions on restricted filesystems
and work with PostgreSQL internals through a SQL API.


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
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*sql
%exclude /usr/lib/.build-id/*
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 1.4.0
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 1.3.4
* Wed Sep 13 2023 Vonng <rh@vonng.com> - 1.2.0
- Initial RPM release, used by Pigsty <https://pigsty.io>