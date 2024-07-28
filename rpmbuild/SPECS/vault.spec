%define debug_package %{nil}
%global pname supabase_vault
%global sname vault
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.9
Release:	1PIGSTY%{?dist}
Summary:	Extension for storing encrypted secrets in the Vault
License:	Apache-2.0
URL:		https://github.com/supabase/%{sname}
Source0:	https://github.com/supabase/%{sname}/archive/refs/tags/vault-0.2.9.tar.gz
#           https://github.com/supabase/vault/archive/refs/tags/v0.2.9.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
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
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 0.2.9
- Initial RPM release, used by Pigsty <https://pigsty.io>