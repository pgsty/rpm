%define debug_package %{nil}
%global pname postbis
%global sname postbis
%global commit ce454ebfbc27e0b6c8357ef6bfc8da1c4b2967c8
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:postbis supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        1PGSTY%{?dist}
Summary:        Biological sequence data types and functions for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/no0p/postbis
Source0:        %{sname}-%{version}.tar.gz
# Source archive: https://github.com/no0p/postbis/archive/ce454ebfbc27e0b6c8357ef6bfc8da1c4b2967c8.tar.gz
Patch0:         postbis-1.0.patch

BuildRequires:  gcc make pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgresql%{pgmajorversion}-devel
Requires:       postgresql%{pgmajorversion}-server

%description
PostBIS provides compact DNA, RNA, amino-acid, and aligned biological
sequence types for PostgreSQL. It also provides sequence functions,
type modifiers, comparison operators, and btree and hash operator classes.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%autosetup -p1 -n %{sname}-%{commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.txt
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Tue Jul 28 2026 Vonng <rh@vonng.com> - 1.0-2PIGSTY
- Fix alphabet output allocation and indexed sequence slice decoding

* Sat Jul 25 2026 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
- Add PostgreSQL 14 through 18 compatibility fixes
