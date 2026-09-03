%global pname supabase_vault
%global sname vault
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
Version:	0.3.1
Release:	1PGSTY%{?dist}
Summary:	Extension for storing encrypted secrets in the Vault
License:	Apache-2.0
URL:		https://github.com/supabase/vault
Source0:	vault-%{version}.tar.gz
#           https://github.com/supabase/vault/archive/refs/tags/v0.3.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  libsodium-devel

%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Supabase provides a table called vault.secrets that can be used to store sensitive information like API keys.
These secrets will be stored in an encrypted format on disk and in any database dumps.
This is often called Encryption At Rest. Decrypting this table is done through a special database
view called vault.decrypted_secrets that uses an encryption key that is itself not avaiable to SQL,
 but can be referred to by ID. Supabase manages these internal keys for you, so you can't leak them out of the database, you can only refer to them by their ids.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.3.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.3.1
- becoming a C extension with solib and llvmjit package
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 0.2.9
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
