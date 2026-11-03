%global pname address_standardizer
%global sname address_standardizer
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}
%{!?runselftest:%global runselftest 0}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:address_standardizer is packaged for PostgreSQL 14 through 18}
%endif

# Propagate %%llvm into PGXS so disabling LLVM also disables bitcode generation.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        3.7.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL extension to parse a US street address string
License:        MIT
URL:            https://github.com/postgis/address_standardizer
Source0:        address_standardizer-%{version}.tar.gz
# https://github.com/postgis/address_standardizer/archive/refs/tags/v3.7.0.tar.gz

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  pcre2-devel
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
%if %runselftest
BuildRequires:  postgresql%{pgmajorversion}-server
BuildRequires:  pgdg-srpm-macros >= 2.0.0
%endif

Requires:       postgresql%{pgmajorversion}-server
Requires:       postgis3_%{pgmajorversion} >= 3.7
Requires:       pcre2

%description
This is a fork of the PAGC standardizer and a single-line address parser.
The code is built into a PostgreSQL extension library and includes the US
address data extension.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} %{with_llvm_arg}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/%{sname}.md

%check
%if %runselftest
%pgdg_check_installcheck %{with_llvm_arg}
%endif

%files
%license COPYING
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_data_us.control
%{pginstdir}/lib/%{sname}.so
%exclude /usr/lib/.build-id/*
%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Mon Nov 02 2026 Ruohang Feng <rh@vonng.com> - 3.7.0-1PGSTY
- Package address_standardizer independently following the PostGIS 3.7 split.
- Keep PGXS LLVM bitcode in the main package with native debug packages.
