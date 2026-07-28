%global pname pgzint
%global sname pgzint
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

# Deferred: active EL repositories only provide Zint 2.11, while pgzint 0.2.0
# requires Zint 2.14 or newer for BARCODE_MEMORY_FILE support.

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgzint only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	Zint barcode generation functions for PostgreSQL
License:	MIT
URL:		https://github.com/davidbeauchamp/pgzint
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgzint/0.2.0/pgzint-0.2.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc zint-devel >= 2.14.0
Requires:	postgresql%{pgmajorversion}-server

%description
pgzint exposes the Zint barcode library to PostgreSQL and returns PNG-formatted
barcodes for the symbologies supported by Zint.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} DOCS= LLVM_BINPATH=%{llvm_binpath}

%files
%license LICENSE
%doc README.md Changes
%{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}-%{version}.index.bc
%{pginstdir}/lib/bitcode/%{pname}-%{version}/
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 27 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- Add RPM package for upstream PGXN 0.2.0
- Require Zint 2.14.0 for BARCODE_MEMORY_FILE support
