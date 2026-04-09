%global pname pgbson
%global sname postgresbson
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
Version:	2.0.2
Release:	1PIGSTY%{?dist}
Summary:	BSON data type and accessor functions for PostgreSQL
License:	MIT
URL:		https://github.com/buzzm/postgresbson
Source0:	%{sname}-%{version}.tar.gz
#		repacked from upstream HEAD e8375bfabcf54de400b07988b6f017d6e48c5a91

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libbson-devel pkgconf-pkg-config
Requires:	postgresql%{pgmajorversion}-server
Requires:	libbson

%description
postgresbson provides the %{pname} PostgreSQL extension, which adds a BSON data
type together with accessor, comparison, and conversion functions.

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
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/postgresbson-2.0.2-avoid-private-libbson-symbol.patch

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} \
  PG_CPPFLAGS="$(pkg-config --cflags libbson-1.0)" \
  BSON_INCLUDES="$(pkg-config --cflags libbson-1.0)" \
  BSON_SHLIB="$(pkg-config --libs libbson-1.0)"

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} \
  PG_CPPFLAGS="$(pkg-config --cflags libbson-1.0)" \
  BSON_INCLUDES="$(pkg-config --cflags libbson-1.0)" \
  BSON_SHLIB="$(pkg-config --libs libbson-1.0)"

%files
%doc README.md LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Tue Apr 07 2026 Vonng <rh@vonng.com> - 2.0.2-1PIGSTY
- Initial RPM release for pgbson, sourced from upstream HEAD e8375bf
- Avoid private libbson symbol dependency for EL9 system libbson
