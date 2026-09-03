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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{rpmname}_%{pgmajorversion}
Version:	1.3
Release:	6PGSTY%{?dist}
Summary:	Textual numeric datatypes for PostgreSQL
License:	GPL-2.0-or-later
URL:		https://github.com/df7cb/postgresql-numeral
Source0:	postgresql-%{pname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 flex bison
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

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

%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{make_passbyvalue}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{make_passbyvalue} install DESTDIR=%{buildroot}

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
* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.3-6PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Rebuild with corrected license metadata.

* Thu Jul 30 2026 Vonng <rh@vonng.com> - 1.3-3PIGSTY
- Align package name with PGDG and obsolete numeral_$v packages
- Force passed-by-value numeral types on 64-bit EL builders
- Build serially to avoid generated parser header races
- Limit PGSTY builds to PostgreSQL 14 through 18

* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
