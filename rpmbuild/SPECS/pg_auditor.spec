%global pname pg_auditor
%global sname pg_auditor
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global source_commit 7c2edff7a09c5882bfc8f1f8aa8f8d5d7e3b0c41
%global source_date 20250228
%global source_short 7c2edff

Name:		%{sname}_%{pgmajorversion}
Version:	0.3
Release:	1.git%{source_date}.%{source_short}PGSTY%{?dist}
Summary:	PostgreSQL extension to log each DML statement and flashback transactions
License:	BSD-3-Clause
URL:		https://github.com/kouber/pg_auditor
Source0:	pg_auditor-%{version}+git%{source_date}.%{source_short}.tar.gz
#           normalized upstream master snapshot 7c2edff7a09c5882bfc8f1f8aa8f8d5d7e3b0c41
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
PostgreSQL auditing extension that records each data modification statement of specific tables,
and allows partial or complete flashback of transactions.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.3-1.git20250228.7c2edffPGSTY
- Pin upstream master snapshot %{source_commit}
- Package the upstream 0.2 to 0.3 SQL upgrade path

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
