%global pname plpgsql_check
%global sname plpgsql_check
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%if 0%{?pgmajorversion} < 14
%{error:plpgsql_check only supports PostgreSQL 14+}
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

Name:		%{sname}_%{pgmajorversion}
Version:	2.9.1
Release:	1PIGSTY%{?dist}
Summary:	Additional tools for PL/pgSQL function validation
License:	MIT
URL:		https://github.com/okbob/plpgsql_check
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/plpgsql_check/2.9.1/plpgsql_check-2.9.1.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
Requires:	postgresql%{pgmajorversion}-server

%description
plpgsql_check provides direct and indirect validation, profiling, tracing, and
dependency inspection tools for PL/pgSQL functions.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

%files
%license LICENSE
%doc README.md TODO.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 04 2026 Vonng <rh@vonng.com> - 2.9.1-1PIGSTY
- Update to upstream PGXN 2.9.1

* Sun May 24 2026 Vonng <rh@vonng.com> - 2.9.0-1PIGSTY
- Initial RPM release for upstream PGXN 2.9.0
