%global pname column_encrypt
%global sname column_encrypt
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	4.0
Release:	1PGSTY%{?dist}
Summary:	Transparent column-level encryption for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/vibhorkum/column_encrypt
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
column_encrypt adds encrypted_text and encrypted_bytea data types for
transparent column-level encryption in PostgreSQL.
It uses the pgcrypto extension for AES encryption, requires
shared_preload_libraries to load its backend hook, and installs objects into
the fixed encrypt schema.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*.bc
%{pginstdir}/lib/bitcode/%{pname}/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 4.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Apr 13 2026 Vonng <rh@vonng.com> - 4.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
