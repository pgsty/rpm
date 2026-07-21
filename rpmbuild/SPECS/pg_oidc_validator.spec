%define debug_package %{nil}
%global pname pg_oidc_validator
%global sname pg_oidc_validator
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_oidc_validator only supports PostgreSQL 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.2
Release:        1PIGSTY%{?dist}
Summary:        OAuth and OIDC token validator for PostgreSQL 18
License:        Apache-2.0
URL:            https://github.com/percona/pg_oidc_validator
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/percona/pg_oidc_validator/archive/refs/tags/0.2.tar.gz

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if 0%{?rhel} == 8 || 0%{?rhel} == 9
BuildRequires:  gcc-toolset-13 gcc-toolset-13-gcc-c++
%else
BuildRequires:  gcc-c++ >= 13
%endif
BuildRequires:  libcurl-devel openssl-devel
Requires:       postgresql%{pgmajorversion}-server

%description
pg_oidc_validator implements PostgreSQL 18's OAuth validator module API. It
discovers OIDC providers, fetches and caches their JWKS data, validates JWT
access tokens, and maps a configured token claim to the PostgreSQL identity.
Load it with oauth_validator_libraries = 'pg_oidc_validator'.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} == 8 || 0%{?rhel} == 9
. /opt/rh/gcc-toolset-13/enable
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 \
    PG_CONFIG=%{pginstdir}/bin/pg_config with_llvm=no %{?_smp_mflags}

%check
readelf -Ws %{pname}.so | grep -q _PG_oauth_validator_module_init

%install
%{__rm} -rf %{buildroot}
%if 0%{?rhel} == 8 || 0%{?rhel} == 9
. /opt/rh/gcc-toolset-13/enable
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 \
    PG_CONFIG=%{pginstdir}/bin/pg_config with_llvm=no install DESTDIR=%{buildroot}

%files
%license LICENSE.txt
%doc README.md
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 0.2-1PIGSTY
- Initial RPM release for Percona pg_oidc_validator 0.2 and PostgreSQL 18
