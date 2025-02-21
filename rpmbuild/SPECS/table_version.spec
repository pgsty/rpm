%define debug_package %{nil}
%global pname table_version
%global sname table_version
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
Version:	1.11.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL table versioning management software

License:	BSD-Like
URL:		https://github.com/linz/postgresql-tableversion
Source0:	postgresql-tableversion-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL table versioning extension, recording row modifications
and its history. The extension provides APIs for accessing snapshots of a table
at certain revisions and the difference generated between any two given
revisions. The extension uses a PL/PgSQL trigger based system to record and
provide access to the row revisions.
This package contains the EXTENSION version of the code (requires access to server filesystem)

%prep
%setup -q -n postgresql-tableversion-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*sql
%{pginstdir}/doc/extension/table_version.md
/usr/local/bin/table_version-loader
/usr/local/share/table_version/table_version-%{version}.sql.tpl

%changelog
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 1.11.0
* Tue Jul 30 2024 Vonng <rh@vonng.com> - 1.10.3
- Initial RPM release, used by Pigsty <https://pigsty.io>