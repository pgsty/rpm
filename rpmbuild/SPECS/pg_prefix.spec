%global sname prefix
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.11
Release:	1PGSTY%{?dist}
License:	PostgreSQL
Summary:	Prefix Range module for PostgreSQL
Source0:	prefix-%{version}.tar.gz

URL:		https://github.com/dimitri/prefix
BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.2.9-2

%description
The prefix project implements text prefix matches operator (prefix @> text)
and provide a GiST opclass for indexing support of prefix searches.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install %{with_llvm_arg} DESTDIR=%{buildroot}
# Rename docs to avoid conflict:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-prefix.md
%{__mv} %{buildroot}%{pginstdir}/doc/extension/TESTS.md %{buildroot}%{pginstdir}/doc/extension/TESTS-prefix.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-prefix.md
%doc %{pginstdir}/doc/extension/TESTS-prefix.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%if %llvm
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.11-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Apr 25 2026 Vonng <rh@vonng.com> - 1.2.11-1PIGSTY
- Update to 1.2.11

* Sat Nov 01 2025 Vonng <rh@vonng.com> - 1.2.10-1PIGSTY
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.2.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
