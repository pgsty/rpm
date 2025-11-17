%global sname prefix
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.10
Release:	1PIGSTY%{?dist}
License:	PostgreSQL
Summary:	Prefix Range module for PostgreSQL
Source0:	prefix-%{version}.tar.gz

URL:		https://github.com/dimitri/prefix
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.2.9-2

%description
The prefix project implements text prefix matches operator (prefix @> text)
and provide a GiST opclass for indexing support of prefix searches.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for prefix
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This package provides JIT support for prefix
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install DESTDIR=%{buildroot}
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
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Nov 01 2025 Vonng <rh@vonng.com> - 1.2.10-1PIGSTY
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.2.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>