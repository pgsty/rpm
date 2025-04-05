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

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	A PostgreSQL extension to add a collection data type
License:	Apache-2.0
URL:		https://github.com/aws/pgcollection
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pgcollection is a memory optimized data type for PostgreSQL. The primary usage is a high performance data structure inside of plpglsql functions. Like other PostgreSQL data types, a collection can be a column of a table, but there are no operators.
A collection is a set of key-value pairs. Each key is a unique string of type text. Entries are stored in creation order. A collection can hold an unlimited number of elements, constrained by the memory available to the database. A collection is stored as a PostgreSQL varlena limiting the maximum size to 1GB if the structure was persisted to a column in a table.
The value of an element can be any PostgreSQL type including composite types with a default of type text. All elements in a collection must be of the same type.

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
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/%{sname}.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 1.0.0
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.9.1
- Initial RPM release, used by Pigsty <https://pigsty.io>