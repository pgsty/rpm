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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.20
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL Extension Whitelisting
License:	PostgreSQL
URL:		https://github.com/dimitri/pgextwlist
Source0:	pgextwlist-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This extension implements extension whitelisting, and will actively prevent users from installing extensions not in the provided list. Also, this extension implements a form of sudo facility in that the whitelisted extensions will get installed as if superuser. Privileges are dropped before handing the control back to the user.
The operations CREATE EXTENSION, DROP EXTENSION, ALTER EXTENSION ... UPDATE, and COMMENT ON EXTENSION are run by superuser. The ALTER EXTENSION ... ADD|DROP command is intentionally not supported so as not to allow users to modify an already installed extension. That means that it's not currently possible to CREATE EXTENSION ... FROM 'unpackaged';.
Note that the extension script is running as if run by a stored procedure owned by your bootstrap superuser and with SECURITY DEFINER, meaning that the extension and all its objects are owned by this superuser.
PostgreSQL versions 10 and later are supported.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/contrib/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Sep 29 2026 Vonng <rh@vonng.com> - 1.20-1PGSTY
- Update to 1.20 with custom-script validation and database-owner restrictions

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.19-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Sep 07 2024 Vonng <rh@vonng.com> - 1.19
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.17
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
