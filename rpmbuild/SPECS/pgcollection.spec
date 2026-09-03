%global pname collection
%global sname pgcollection
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
Version:	2.1.3
Release:	1PGSTY%{?dist}
Summary:	A PostgreSQL extension to add a collection data type
License:	Apache-2.0
URL:		https://github.com/aws/pgcollection
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pgcollection-2.1.3.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pgcollection is a memory optimized data type for PostgreSQL. The primary usage is a high performance data structure inside of plpglsql functions. Like other PostgreSQL data types, a collection can be a column of a table, but there are no operators.
A collection is a set of key-value pairs. Each key is a unique string of type text. Entries are stored in creation order. A collection can hold an unlimited number of elements, constrained by the memory available to the database.
A collection is stored as a PostgreSQL varlena limiting the maximum size to 1GB if the structure was persisted to a column in a table.
The value of an element can be any PostgreSQL type including composite types with a default of type text. All elements in a collection must be of the same type.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/%{sname}.md

%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.1.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 2.1.3
- Share the LLVM generated-header dependency patch with DEB packaging

* Sat Mar 21 2026 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.1.1-1PIGSTY
- https://github.com/aws/pgcollection/releases/tag/v1.1.1
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.9.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
