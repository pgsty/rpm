%global sname pg_rewrite

%global pgrwmajver 2
%global pgrwmidver 2
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	PostgreSQL tool to rewrite a table
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgrwmajver}.%{pgrwmidver}
Release:	1PGSTY%{?dist}
License:	PostgreSQL
URL:		https://github.com/cybertec-postgresql/%{sname}
Source0:	pg_rewrite-REL%{pgrwmajver}_%{pgrwmidver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_rewrite is a tool to rewrite table (i.e. to copy its data to a new file).
It allows both read and write access to the table during the rewriting.

%prep
%setup -q -n %{sname}-REL%{pgrwmajver}_%{pgrwmidver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%{pginstdir}/lib/%{sname}*.*
%{pginstdir}/share/extension/%{sname}*.*

%if %llvm
    %{pginstdir}/lib/bitcode/%{sname}.index.bc
    %{pginstdir}/lib/bitcode/%{sname}/*bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jul 23 2026 Vonng <rh@vonng.com> - 2.2-1PIGSTY
- https://github.com/cybertec-postgresql/pg_rewrite/releases/tag/REL2_2
* Sun Sep 07 2025 Ruohang Feng <rh@vonng.com> - 2.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
