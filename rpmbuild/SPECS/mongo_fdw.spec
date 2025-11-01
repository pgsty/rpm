%global sname mongo_fdw

%global mongofdwmajver 5
%global mongofdwmidver 5
%global mongofdwminver 3
%global relver %{mongofdwmajver}_%{mongofdwmidver}_%{mongofdwminver}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	%{mongofdwmajver}.%{mongofdwmidver}.%{mongofdwminver}
Release:	1PIGSTY%{?dist}
License:	LGPLv3
Summary:	PostgreSQL foreign data wrapper for MongoDB
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	%{sname}-REL-%{relver}.tar.gz
Source1:	%{sname}-config.h

BuildRequires:	postgresql%{pgmajorversion}-devel

%if 0%{?suse_version} >= 1499
Requires:		libsnappy1 libbson-1_0-0 libmongoc-1_0-0
BuildRequires:		snappy-devel libbson-1_0-0-devel libmongoc-1_0-0-devel
BuildRequires:		libopenssl-devel
%else
Requires:	snappy
Requires:	mongo-c-driver-libs libbson
BuildRequires:	mongo-c-driver-devel snappy-devel
BuildRequires:	openssl-devel cyrus-sasl-devel krb5-devel
BuildRequires:	libbson-devel
%endif

Requires:	postgresql%{pgmajorversion}-server cyrus-sasl-lib

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for MongoDB.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for mongo_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for mongo_fdw
%endif

%prep
%setup -q -n %{sname}-REL-%{relver}

%build
sh autogen.sh

%if 0%{?fedora} || 0%{?rhel} >= 8
sed -i "s:^\(PG_CPPFLAGS.*\):\1 -I/usr/include/json-c -fPIC:g" Makefile
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.c
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.h
sed -i "s:\(^#include \"bson.h\"\)://\1:g" mongo_wrapper.h
%endif

PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/json-c/*.bc
%endif

%changelog
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 5.5.3
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>