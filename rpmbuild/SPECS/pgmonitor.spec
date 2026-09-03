%global pname pgmonitor
%global sname pgmonitor
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgmonitor only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.2.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL metrics for external collectors
License:        Apache-2.0
URL:            https://github.com/CrunchyData/pgmonitor-extension
Source0:        pgmonitor-extension-%{version}.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pgmonitor provides collector-friendly metric views, materialized views,
tables, and an optional background worker to refresh stored metrics.

%prep
%setup -q -n pgmonitor-extension-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/pgmonitor_bgw.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/src/pgmonitor_bgw.index.bc
%{pginstdir}/lib/bitcode/src/pgmonitor_bgw/src/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.2.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 2.2.0-1PIGSTY
- Initial RPM release for upstream 2.2.0
