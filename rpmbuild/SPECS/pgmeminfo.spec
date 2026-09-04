%global pname pgmeminfo
%global sname pgmeminfo
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.1
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension to allow to access to memory usage diagnostics
License:	MIT
URL:		https://github.com/okbob/%{sname}
Source0:	%{sname}-VERSION_1_0_1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
The pgmeminfo extension can be used to display memory usage information of a PostgreSQL server.

%prep
%setup -q -n %{sname}-VERSION_1_0_1

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.0.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to VERSION_1_0_1

* Sat Nov 02 2024 Vonng <rh@vonng.com> - 1.0.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
