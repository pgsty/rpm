%global pname pg_vault_tde
%global sname pg_vault_tde
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_vault_tde only supports PostgreSQL 17 through 18 in PGSTY builds}
%endif

%if 0%{?rhel} && 0%{?rhel} < 9
%{error:pg_vault_tde requires OpenSSL 3 and is only supported on EL9 and EL10}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.7.1
Release:	1PGSTY%{?dist}
Summary:        Transparent Data Encryption for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/labmiriade/pg_vault_tde
Source0:        %{sname}-%{version}.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make pkgconfig openssl-devel >= 3.0 libcurl-devel chrpath
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server openssl-libs >= 3.0 libcurl

%description
pg_vault_tde provides Transparent Data Encryption through custom table and
index access methods. It supports HashiCorp Vault, OpenBao, local wallets, and
PKCS#11 key providers. The module must be configured in
shared_preload_libraries before CREATE EXTENSION pg_vault_tde.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
  PG_CONFIG=%{pginstdir}/bin/pg_config \
  CFLAGS="%{optflags} -fno-lto"

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot} \
  PG_CONFIG=%{pginstdir}/bin/pg_config
chrpath -d %{buildroot}%{pginstdir}/lib/%{pname}.so

%files
%license LICENSE
%doc README.md doc/pg_vault_tde.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/bin/pg_dump_tde
%{pginstdir}/bin/pg_restore_tde
%{pginstdir}/bin/pg_basebackup_tde
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 1.7.1-1PGSTY
- Update to 1.7.1

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.7.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 1.7.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.7.0
- Package PostgreSQL 17 and 18 on EL9/EL10 with OpenSSL 3 and libcurl
- Package the versioned TDE backup tools and honor DESTDIR during install
