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

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.1
Release:	1PIGSTY%{?dist}
Summary:	Extension for storing encrypted secrets in the Vault
License:	Apache-2.0
URL:		https://github.com/supabase/vault
Source0:	vault-%{version}.tar.gz
#           https://github.com/supabase/vault/archive/refs/tags/v0.3.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  libsodium-devel

Requires:	postgresql%{pgmajorversion}-server

%description
Supabase provides a table called vault.secrets that can be used to store sensitive information like API keys.
These secrets will be stored in an encrypted format on disk and in any database dumps.
This is often called Encryption At Rest. Decrypting this table is done through a special database
view called vault.decrypted_secrets that uses an encryption key that is itself not avaiable to SQL,
 but can be referred to by ID. Supabase manages these internal keys for you, so you can't leak them out of the database, you can only refer to them by their ids.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.3.1
- becoming a C extension with solib and llvmjit package
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 0.2.9
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>