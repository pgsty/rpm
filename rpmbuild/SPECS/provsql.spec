%define debug_package %{nil}
%global _build_id_links none
%global pname provsql
%global sname provsql
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14
%{error:provsql only supports PostgreSQL 14+}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.10.0
Release:	1PIGSTY%{?dist}
Summary:	Semiring provenance and uncertainty management for PostgreSQL
License:	MIT
URL:		https://github.com/PierreSenellart/provsql
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++ boost-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
ProvSQL adds semiring provenance and uncertainty management to PostgreSQL.
It rewrites queries to track tuple provenance and provides probability,
Shapley value, where-provenance, and temporal provenance evaluation.

ProvSQL must be loaded through shared_preload_libraries before running
CREATE EXTENSION provsql CASCADE.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?rhel} == 8
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}-el8-to_chars.patch
%endif

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} with_llvm=no

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} with_llvm=no

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/doc/extension/%{pname}.md

%changelog
* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.10.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.10.0/
- Refresh the EL8 std::to_chars compatibility patch

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 1.9.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.9.0/
- Refresh the EL8 std::to_chars compatibility patch

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 1.8.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.8.0/

* Sun May 24 2026 Vonng <rh@vonng.com> - 1.7.1-1PIGSTY
- https://pgxn.org/dist/provsql/1.7.1/
* Thu May 14 2026 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.4.0/
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.2.3-1PIGSTY
- https://github.com/PierreSenellart/provsql/releases/tag/v1.2.3
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.2.2-1PIGSTY
- Restrict builds to PostgreSQL 14+ to match extension metadata and tested support
- Initial RPM release
- https://github.com/PierreSenellart/provsql/releases/tag/v1.2.2
