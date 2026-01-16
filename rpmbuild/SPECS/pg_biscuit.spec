%global pname biscuit
%global sname pg_biscuit
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	2.2.2
Release:	1PIGSTY%{?dist}
Summary:	IAM-LIKE pattern matching with bitmap indexing
License:	MIT
URL:		https://github.com/CrystallineCore/Biscuit
Source0:	Biscuit-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
Biscuit is a PostgreSQL Index Access Method (IAM) for high-performance pattern matching
on text columns. Biscuit indexes are specifically designed to accelerate LIKE queries with
arbitrary wildcards using roaring bitmaps. It provides superior performance for wildcard
pattern matching compared to traditional B-tree, GIN, or GiST indexes, especially for
queries with leading wildcards like '%%pattern%%'.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
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
%setup -q -n Biscuit-%{version}

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
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 2.2.2-1PIGSTY
* Tue Dec 16 2025 Vonng <rh@vonng.com> - 2.0.1-1PIGSTY
- repo goes to https://github.com/CrystallineCore/Biscuit
* Tue Nov 18 2025 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
