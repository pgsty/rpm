%global sname pgl_ddl_deploy
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        2.2.1
Release:        1PIGSTY%{?dist}
Summary:        Transparent DDL replication for PostgreSQL
License:        MIT
URL:            https://github.com/enova/%{sname}
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pgl_ddl_deploy-2.2.1-pg18.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
Requires:       postgresql%{pgmajorversion}-server

%description
pgl_ddl_deploy provides transparent DDL replication for PostgreSQL using
pglogical or native logical replication.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?pgmajorversion} >= 18
%patch -P 0 -p1
%endif

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/ddl_deparse.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*
%{pginstdir}/lib/bitcode/ddl_deparse*
%endif

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 2.2.1-1PIGSTY
- Initial RPM release with PostgreSQL 18 compatibility
