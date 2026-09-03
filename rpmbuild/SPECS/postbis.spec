%global pname postbis
%global sname postbis
%global commit ce454ebfbc27e0b6c8357ef6bfc8da1c4b2967c8
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:postbis supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
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
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
PostBIS provides compact DNA, RNA, amino-acid, and aligned biological
sequence types for PostgreSQL. It also provides sequence functions,
type modifiers, comparison operators, and btree and hash operator classes.

%prep
%autosetup -p1 -n %{sname}-%{commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.txt
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Jul 28 2026 Vonng <rh@vonng.com> - 1.0-2PIGSTY
- Fix alphabet output allocation and indexed sequence slice decoding

* Sat Jul 25 2026 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
- Add PostgreSQL 14 through 18 compatibility fixes
