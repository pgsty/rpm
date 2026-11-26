%global sname multicorn2
%global pname multicorn
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global python3_pkgversion 3.12
%global __python3 %{_bindir}/python3.12
%global __ospython %{__python3}
%global mcsite %{_libdir}/python3.12/site-packages
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} != 19
%{error:This Multicorn recipe targets PostgreSQL 19}
%endif

%if %llvm
# Use the distribution's paired clang and thin-linker even when a builder
# overrides the LLVM directory embedded in PGXS.
%global llvm_arg LLVM_BINPATH=%{_bindir} CLANG=%{_bindir}/clang
%else
%global llvm_arg with_llvm=no
%endif
%global pgxs_args PG_CONFIG=%{pginstdir}/bin/pg_config PYTHON_OVERRIDE=%{__python3} enable_rpath=no %{llvm_arg}

Name:           %{sname}_%{pgmajorversion}
Version:        3.2
Release:        1PGSTY%{?dist}
Summary:        Python foreign data wrappers for PostgreSQL %{pgmajorversion}
License:        PostgreSQL
URL:            https://github.com/pgsql-io/multicorn2
Source0:        %{sname}-%{version}.tar.gz
Patch0:         multicorn-3.2-pg19-python.patch

BuildRequires:  postgresql%{pgmajorversion}-devel >= 19.0
BuildRequires:  gcc make patch binutils /usr/bin/python3.12-config
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server%{?_isa} >= 19.0
Requires:       python(abi) = 3.12
Provides:       %{sname} = %{version}
Provides:       python3dist(multicorn)%{?_isa} = %{version}-%{release}

%description
Multicorn runs Python foreign data wrappers in PostgreSQL. Its native
logging and interrupt helpers are built into the PostgreSQL-specific
library. On PostgreSQL 19, use Multicorn and PL/Python in separate
backend sessions. Wrappers that use the plpy SPI module require PL/Python
integration and are unsupported in this build.

%prep
# This archive also ships as v3.2.tar.gz in the signed PGDG 3.2 SRPM.
echo 'e31e8f6e25acafd0dc8a2faf90a8c1e29e114abe8383e5c1041f54ab0f9bb44f  %{SOURCE0}' | sha256sum -c -
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1 -F0

%build
%make_build %{pgxs_args}

%install
# Upstream's python_code target upgrades pip and installs on the build host.
# Package the shared Python sources with PGDG-compatible paths and timestamps.
%make_install -o python_code %{pgxs_args}
install -d %{buildroot}%{mcsite}/%{pname}
cp -pr python/%{pname}/. %{buildroot}%{mcsite}/%{pname}/

%check
readelf -d %{buildroot}%{pginstdir}/lib/%{pname}.so | grep -F 'libpython3.12.so.1.0'
test -f %{buildroot}%{mcsite}/%{pname}/csvfdw.py

%files
%license LICENSE
%doc README.md
%doc %{pginstdir}/doc/extension/%{pname}.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--%{version}.sql
%{mcsite}/%{pname}/
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Wed Nov 25 2026 Vonng <rh@vonng.com> - 3.2-1PGSTY
- Package Multicorn for PostgreSQL 19 with Python 3.12
- Embed the native helper in the backend library and package PGXS bitcode
