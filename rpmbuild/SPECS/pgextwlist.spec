%global pname pgextwlist
%global sname pgextwlist
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
Version:	1.19
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Extension Whitelisting
License:	PostgreSQL
URL:		https://github.com/dimitri/pgextwlist
Source0:	pgextwlist-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
This extension implements extension whitelisting, and will actively prevent users from installing extensions not in the provided list. Also, this extension implements a form of sudo facility in that the whitelisted extensions will get installed as if superuser. Privileges are dropped before handing the control back to the user.
The operations CREATE EXTENSION, DROP EXTENSION, ALTER EXTENSION ... UPDATE, and COMMENT ON EXTENSION are run by superuser. The ALTER EXTENSION ... ADD|DROP command is intentionally not supported so as not to allow users to modify an already installed extension. That means that it's not currently possible to CREATE EXTENSION ... FROM 'unpackaged';.
Note that the extension script is running as if run by a stored procedure owned by your bootstrap superuser and with SECURITY DEFINER, meaning that the extension and all its objects are owned by this superuser.
PostgreSQL versions 10 and later are supported.

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
Requires:	llvm => 17.0
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
%{pginstdir}/lib/%{pname}.so
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/contrib/README.md

%changelog
* Sun Sep 07 2024 Vonng <rh@vonng.com> - 1.19
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.17
- Initial RPM release, used by Pigsty <https://pigsty.io>