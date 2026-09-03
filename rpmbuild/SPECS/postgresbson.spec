%global pname pgbson
%global sname postgresbson
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:postgresbson only supports PostgreSQL 14 through 18 in PGSTY builds}
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

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.0
Release:	1PGSTY%{?dist}
Summary:	BSON data type and accessor functions for PostgreSQL
License:	MIT
URL:		https://github.com/buzzm/postgresbson
Source0:	%{sname}-%{version}.tar.gz
#		normalized from https://api.pgxn.org/dist/bson/2.1.0/bson-2.1.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libbson-devel pkgconf-pkg-config
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	libbson

%description
postgresbson provides the %{pname} PostgreSQL extension, which adds a BSON data
type together with accessor, comparison, and conversion functions.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/postgresbson-2.1.0.patch

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
  PG_CPPFLAGS="$(pkg-config --cflags libbson-1.0)" \
  BSON_INCLUDES="$(pkg-config --cflags libbson-1.0)" \
  BSON_SHLIB="$(pkg-config --libs libbson-1.0)"

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} \
  PG_CPPFLAGS="$(pkg-config --cflags libbson-1.0)" \
  BSON_INCLUDES="$(pkg-config --cflags libbson-1.0)" \
  BSON_SHLIB="$(pkg-config --libs libbson-1.0)"

%files
%doc README.md LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 2.1.0-1PIGSTY
- Update to upstream PGXN bson 2.1.0
- Refresh the system libbson compatibility fix
- Restrict builds to active PostgreSQL 14 through 18 releases

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 2.0.4-1PIGSTY
- Update to upstream PGXN bson 2.0.4
- Keep the system libbson compatibility fix for ISO-8601 date formatting

* Tue Apr 07 2026 Vonng <rh@vonng.com> - 2.0.2-1PIGSTY
- Initial RPM release for pgbson, sourced from upstream HEAD e8375bf
- Avoid private libbson symbol dependency for EL9 system libbson
