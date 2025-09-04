%global pname toastinfo
%global sname toastinfo
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
Version:	1.5
Release:	1PIGSTY%{?dist}
Summary:	Show storage structure of varlena datatypes in PostgreSQL
License:	BSD 2-Clause
URL:		https://github.com/credativ/toastinfo
Source0:	toastinfo-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension exposes the internal storage structure of variable-length datatypes, called varlena.
The function pg_toastinfo describes the storage form of a datum:
null for NULLs
ordinary for non-varlena datatypes
short inline varlena for varlena values up to 126 bytes (1 byte header)
long inline varlena, (un)compressed for varlena values up to 1GiB (4 bytes header)
toasted varlena, (un)compressed for varlena values up to 1GiB stored in TOAST tables
compressed varlenas show the compression method (pglz, lz4) in PG14+
The function pg_toastpointer returns a varlena's chunk_id oid in the corresponding TOAST table. It returns NULL on non-varlena input.


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
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 1.5
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.4
- Initial RPM release, used by Pigsty <https://pigsty.io>