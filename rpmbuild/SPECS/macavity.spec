%global sname macavity
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:macavity supports PostgreSQL 16-18}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.2.0
Release:        1PGSTY%{?dist}
Summary:        Deterministic fault injection for PostgreSQL test clusters
License:        MIT
URL:            https://github.com/CrystallineCore/Macavity
Source0:        %{sname}-%{version}.tar.gz
# Upstream tag source: https://codeload.github.com/CrystallineCore/Macavity/tar.gz/refs/tags/v0.2.0

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
macavity injects session-local errors, delays and backend crashes at named
PostgreSQL execution points. This destructive testing extension is intended
only for development and disposable test clusters.

%prep
%setup -q -n macavity-0.2.0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} DOCS=

%install
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot} DOCS=

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/lib/%{sname}.so
%if %llvm
%{pginstdir}/lib/bitcode/%{sname}/
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%endif

%changelog
* Tue Sep 29 2026 Vonng <rh@vonng.com> - 0.2.0-1PGSTY
- Update to upstream 0.2.0
- Keep the PGXN testing status and disposable-cluster scope

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Package upstream 0.1.0 for PostgreSQL 16 through 18
- Package the testing release for disposable test clusters only
