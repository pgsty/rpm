%global pname numeral
%global sname numeral
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
Version:	1.3
Release:	1PIGSTY%{?dist}
Summary:	Textual numeric datatypes for PostgreSQL
License:	GPL
URL:		https://github.com/df7cb/postgresql-numeral
Source0:	%{pname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 flex bison
Requires:	postgresql%{pgmajorversion}-server

%description
Christoph Berg cb@df7cb.de
postgresql-numeral provides numeric data types for PostgreSQL that use numerals (words instead of digits) for input and output.
Data types:
numeral: English numerals (one, two, three, four, ...), short scale (10⁹ = billion)
zahl: German numerals (eins, zwei, drei, vier, ...), long scale (10⁹ = Milliarde)
roman: Roman numerals (I, II, III, IV, ...)
Requires PostgreSQL >= 9.4 (currently up to 13) and Bison 3.

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
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>