%global pname numeral
%global sname numeral
%global rpmname postgresql-numeral
%global oldname numeral_%{pgmajorversion}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:numeral only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%ifarch x86_64 aarch64
%global make_passbyvalue PASSEDBYVALUE=passedbyvalue,
%else
%global make_passbyvalue %{nil}
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{rpmname}_%{pgmajorversion}
Version:	1.3
Release:	1PGSTY%{?dist}
Summary:	Textual numeric datatypes for PostgreSQL
License:	LicenseRef-Upstream-No-License
URL:		https://github.com/df7cb/postgresql-numeral
Source0:	postgresql-%{pname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 flex bison
Requires:	postgresql%{pgmajorversion}-server
Provides:	%{oldname} = %{version}-%{release}
Provides:	%{oldname}%{?_isa} = %{version}-%{release}
Obsoletes:	%{oldname} < %{version}-%{release}

%description
Christoph Berg cb@df7cb.de
postgresql-numeral provides numeric data types for PostgreSQL that use numerals (words instead of digits) for input and output.
Data types:
numeral: English numerals (one, two, three, four, ...), short scale (10⁹ = billion)
zahl: German numerals (eins, zwei, drei, vier, ...), long scale (10⁹ = Milliarde)
roman: Roman numerals (I, II, III, IV, ...)
PGSTY packages target PostgreSQL 14 through 18.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{oldname}-llvmjit = %{version}-%{release}
Provides:	%{oldname}-llvmjit%{?_isa} = %{version}-%{release}
Obsoletes:	%{oldname}-llvmjit < %{version}-%{release}
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
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{make_passbyvalue}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{make_passbyvalue} install DESTDIR=%{buildroot}

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
* Thu Jul 30 2026 Vonng <rh@vonng.com> - 1.3-3PIGSTY
- Align package name with PGDG and obsolete numeral_$v packages
- Force passed-by-value numeral types on 64-bit EL builders
- Build serially to avoid generated parser header races
- Limit PGSTY builds to PostgreSQL 14 through 18

* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
