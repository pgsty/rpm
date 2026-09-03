%global sname pgl_ddl_deploy
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.2.1
Release:        1PGSTY%{?dist}
Summary:        Transparent DDL replication for PostgreSQL
License:        MIT
URL:            https://github.com/enova/%{sname}
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pgl_ddl_deploy-2.2.1.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pgl_ddl_deploy provides transparent DDL replication for PostgreSQL using
pglogical or native logical replication.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?pgmajorversion} >= 18
%patch -P 0 -p1
%endif

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/ddl_deparse.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*
%{pginstdir}/lib/bitcode/ddl_deparse*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.2.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Jul 22 2026 Vonng <rh@vonng.com> - 2.2.1-1PIGSTY
- Initial RPM release with PostgreSQL 18 compatibility
