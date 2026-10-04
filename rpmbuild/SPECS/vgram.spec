%global pname vgram
%global sname vgram
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:vgram only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PGSTY%{?dist}
Summary:        Variable-length gram indexes for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/akorotkov/vgram
Source0:        vgram-1.0-babae3775c9c.tar.gz
# Source: https://codeload.github.com/akorotkov/vgram/tar.gz/babae3775c9c21bcf66f55c434642af3eeb0ce0d
# SHA256: 354850de1e59de355ad3fe26239b88be5e8ec6cb935cf5cfa73e6c74fb98988d

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Variable-length gram indexes for PostgreSQL.

%prep
%setup -q -n vgram-babae3775c9c21bcf66f55c434642af3eeb0ce0d

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.0-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
