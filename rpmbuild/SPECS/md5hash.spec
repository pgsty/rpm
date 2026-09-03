%global pname md5hash
%global sname md5hash
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
Version:	1.0.1
Release:	1PGSTY%{?dist}
Summary:	A custom data type for storing MD5 hashes (instead of the native TEXT varlena type).
License:	BSD-2-Clause
URL:		https://github.com/tvondra/md5hash
Source0:	md5hash-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This extension provides a simple data type storing 128-bit values (e.g. MD5 hashes) in a bit more efficient way - in a fixed-length columns and inline.
The extension defines the 'md5hash' type itself, casts, operators and an operator class for btree indexes. It's fairly straightforward and simple to add more operators or classes.

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
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun May 05 2024 Vonng <rh@vonng.com> - 1.0.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
