%global sname orioledb
%define debug_package %{nil}
%define _build_id_links none
%global pname orioledb
%{!?pgmajorversion:%global pgmajorversion 18}
%if 0%{?pgmajorversion} == 18
%global orioledb_patchset 1
%global upstream_pgver 18.4
%else
%if 0%{?pgmajorversion} == 17
%global orioledb_patchset 20
%global upstream_pgver 17.9
%else
%if 0%{?pgmajorversion} == 16
%global orioledb_patchset 47
%global upstream_pgver 16.13
%else
%{error:orioledb beta16 packaging supports PostgreSQL 16, 17, and 18 only}
%endif
%endif
%endif
%global pginstdir	/usr/oriole-%{pgmajorversion}
%global orioledb_beta beta16

Name:		%{sname}_%{pgmajorversion}
Version:	1.8
Release:	beta16PIGSTY%{?dist}
Summary:	Modern cloud-native storage engine for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/orioledb/orioledb
Source0:	%{sname}-%{orioledb_beta}.tar.gz

BuildRequires:	oriolepg_%{pgmajorversion} = %{pgmajorversion}.%{orioledb_patchset}
BuildRequires:	libcurl-devel, libzstd-devel, openssl-devel
Requires:	oriolepg_%{pgmajorversion} = %{pgmajorversion}.%{orioledb_patchset}

%description
OrioleDB – building a modern cloud-native storage engine, and solving some PostgreSQL wicked problems
This is the extension package for OrioleDB beta 16 on OriolePG %{pgmajorversion}.%{orioledb_patchset}
(PostgreSQL %{upstream_pgver}, patchset %{orioledb_patchset})

%prep
%setup -q -n %{sname}-%{orioledb_beta}

%build
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 ORIOLEDB_PATCHSET_VERSION=%{orioledb_patchset} %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 ORIOLEDB_PATCHSET_VERSION=%{orioledb_patchset} %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/postgresql/%{pname}.so
%{pginstdir}/share/postgresql/extension/%{pname}.control
%{pginstdir}/share/postgresql/extension/%{pname}*sql

%changelog
* Fri Jun 19 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.8-beta16PIGSTY
- Update to upstream beta16
- Require matching OriolePG beta16 patchsets for PG16/PG17/PG18

* Thu Apr 16 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.7-0.beta15PIGSTY
- Update to upstream beta15
- Require OriolePG 17.18 built from the PostgreSQL 17.7-based OrioleDB patchset

* Thu Feb 26 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 1.6-0.beta14PIGSTY
* Thu Jul 24 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.5-0.beta12PIGSTY
* Tue May 27 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.4-0.beta11PIGSTY
* Sat Apr 05 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.4-0.beta10PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
