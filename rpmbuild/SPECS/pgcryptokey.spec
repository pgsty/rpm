%global pname pgcryptokey
%global sname pgcryptokey
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.85
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL table versioning extension
License:	PostgreSQL
URL:		http://momjian.us/download/%{sname}/
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
pgcryptokey allows the creation, selection, rotation, and deletion of
cryptographic data keys. Each cryptographic data key is encrypted/decrypted
with (i.e., wrapped inside) an access password. Accessing a cryptographic
data key requires the proper access password.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc README
%license LICENSE
%{pginstdir}/lib/%{pname}_acpass.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/extension/%{sname}_acpass.sample

%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}_acpass/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.85-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Nov 02 2024 Vonng <rh@vonng.com> - 0.85
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
