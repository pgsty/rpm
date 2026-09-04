%global sname	sqlite_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	SQLite Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.5.0
Release:	1PGSTY%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgspider/%{sname}
Source0:	%{sname}-%{version}.tar.gz
Patch0:		sqlite_fdw-2.5.0-pg18.patch
Patch1:		sqlite_fdw-2.5.0-el8-sqlite.patch
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server sqlite-devel
#BuildRequires:	libspatialite-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
#Requires:	libspatialite

%if 0%{?suse_version} >= 1500
# Unfortunately SLES 15 ships the libraries with -devel subpackage:
Requires:	sqlite3-devel >= 3.7
%else
# All other sane distributions have a separate -libs subpackage:
Requires:	sqlite-libs >= 3.7
%endif

%description
This PostgreSQL extension is a Foreign Data Wrapper for SQLite.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?pgmajorversion} >= 18
%patch -P 0 -p1
%endif
%if 0%{?rhel} == 8
%patch -P 1 -p1
%endif

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.5.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Jul 22 2026 Vonng <rh@vonng.com> - 2.5.0-3PIGSTY
- Add PostgreSQL 18 compatibility, safe LIMIT pushdown, and EL8 SQLite support

* Thu May 22 2025 Vonng <rh@vonng.com> - 2.5.0-2PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
