%global pname codesystem
%global sname codesystem
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:codesystem is packaged for PostgreSQL 14 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.2.1
Release:        1PGSTY%{?dist}
Summary:        Validated, ordered and hierarchical classification codes
License:        BSD-2-Clause
URL:            https://github.com/John-Cameron-Burns/pg-codesystem
Source0:        %{sname}-%{version}.tar.gz
# https://github.com/John-Cameron-Burns/pg-codesystem/archive/refs/tags/v0.2.1.tar.gz

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
codesystem stores classification codes as compact, validated values with
hierarchy, ordering, revisions and mappings between related code systems.
The upstream 0.2.1 distribution retains SQL extension version 0.2.0.

%prep
%setup -q -n pg-codesystem-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md docs
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 0.2.1-1PGSTY
- Initial RPM release with upstream SQL extension version 0.2.0
- Preserve PGXS bitcode and native debug packages
