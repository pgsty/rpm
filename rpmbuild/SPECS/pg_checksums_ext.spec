%global pname pg_checksums
%global sname pg_checksums_ext
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_checksums_ext is packaged for PostgreSQL 14 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.3.1
Release:        1PGSTY%{?dist}
Summary:        Multi-level data integrity checksum functions for PostgreSQL
License:        MIT
URL:            https://github.com/VictorNagibator/pg_checksums
Source0:        %{pname}-%{version}.tar.gz
# https://api.github.com/repos/VictorNagibator/pg_checksums/tarball/v1.3.1
# Normalize the official tag archive root with GNU tar.

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
pg_checksums provides SQL checksum functions for pages, cells, tuples,
tables, indexes and databases, with physical and logical variants.
This extension is separate from the PGDG pg_checksums command-line tool.

%prep
%setup -q -n %{pname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md Changes
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Sat Oct 24 2026 Ruohang Feng <rh@vonng.com> - 1.3.1-1PGSTY
- Initial RPM release for PostgreSQL 14 through 18.
- Include PGXS bitcode and retain debuginfo and debugsource packages.
- Use a distinct package name to coexist with the PGDG checksum utility.
