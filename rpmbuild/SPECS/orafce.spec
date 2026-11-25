%global pname orafce
%global sname orafce
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:orafce is packaged for PostgreSQL 15 through 19}
%endif

%if %llvm
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        4.17.2
Release:        1PGSTY%{?dist}
Summary:        Oracle-compatible functions and packages for PostgreSQL
License:        0BSD
URL:            https://github.com/orafce/orafce
Source0:        %{sname}-%{version}.tar.gz
# Official archive: https://codeload.github.com/orafce/orafce/tar.gz/refs/tags/VERSION_4_17_2
# SHA256: 0578c82efbe4e088fd0fe5680122e8743d710b0b97a57e05000fa5c437ba5500

BuildRequires:  bison flex gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Orafce implements Oracle-compatible SQL functions, operators and packages in PostgreSQL.

%prep
%setup -q -n orafce-VERSION_4_17_2

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%{pginstdir}/doc/extension/*
%license LICENSE COPYRIGHT.orafce
%doc README.asciidoc INSTALL.orafce
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif
%exclude /usr/lib/.build-id

%changelog
* Wed Nov 25 2026 Ruohang Feng <rh@vonng.com> - 4.17.2-1PGSTY
- Package upstream 4.17.2 for PostgreSQL 15 through 19.
