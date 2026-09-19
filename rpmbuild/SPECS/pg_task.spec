%global pname pg_task
%global sname pg_task
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_task only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	3.0.0
Release:	1PGSTY%{?dist}
Summary:	Background SQL task scheduler for PostgreSQL
License:	MIT
URL:		https://github.com/RekGRpth/pg_task
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_task/3.0.0/pg_task-3.0.0.zip
Patch0:		pg_task-3.0.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc curl
BuildRequires:	pcre2-tools
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif
Requires:	postgresql%{pgmajorversion}-server

%description
pg_task is a PostgreSQL background worker that executes scheduled SQL tasks
asynchronously. It is loaded through shared_preload_libraries and does not
install a CREATE EXTENSION control file.

%prep
%setup -q -n %{sname}-%{version}
chmod 0755 postgres.sh exec.sh latch.sh
patch -p1 --forward --batch --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} %{with_llvm_arg}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 3.0.0-1PGSTY
- Update to 3.0.0
- Include the PGXS compatibility patch in the source RPM
- Use portable curl flags and bounded downloads with the EL8 curl client
- Keep downloaded PostgreSQL source within the target major version

* Fri Jun 12 2026 Vonng <rh@vonng.com> - 2.1.29-1PIGSTY
- Build postgres.c with pcre2grep in EL builders

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 2.1.29-1PIGSTY
- Initial RPM release for upstream PGXN 2.1.29
