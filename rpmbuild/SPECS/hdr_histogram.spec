%global pname hdr_histogram
%global sname hdr_histogram
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:hdr_histogram only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.0
Release:        1PGSTY%{?dist}
Summary:        HDR histogram type and mergeable percentile aggregates
License:        MIT AND CC0-1.0
URL:            https://github.com/vovcke/pg_hdr_histogram
Source0:        %{sname}-%{version}.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  zlib-devel
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Stores compressed HDR histograms as a PostgreSQL type and provides aggregates
and scalar functions to build, merge and query bounded-error percentiles.
Includes the vendored HdrHistogram_c implementation.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE third_party/HdrHistogram_c/NOTICE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 1.0.0-1PGSTY
- Initial RPM release for PostgreSQL 14-18
