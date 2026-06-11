%define debug_package %{nil}
%global pname pg_task
%global sname pg_task
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_task only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.29
Release:	1PIGSTY%{?dist}
Summary:	Background SQL task scheduler for PostgreSQL
License:	MIT
URL:		https://github.com/RekGRpth/pg_task
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_task/2.1.29/pg_task-2.1.29.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
Requires:	postgresql%{pgmajorversion}-server

%description
pg_task is a PostgreSQL background worker that executes scheduled SQL tasks
asynchronously. It is loaded through shared_preload_libraries and does not
install a CREATE EXTENSION control file.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} with_llvm=no

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} with_llvm=no

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 11 2026 Vonng <rh@vonng.com> - 2.1.29-1PIGSTY
- Initial RPM release for upstream PGXN 2.1.29
