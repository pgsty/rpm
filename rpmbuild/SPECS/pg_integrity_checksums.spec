%global pname pg_integrity_checksums
%global sname pg_integrity_checksums
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_integrity_checksums is packaged for PostgreSQL 14 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.0.0
Release:        1PGSTY%{?dist}
Summary:        Physical and logical data checksums for PostgreSQL
License:        MIT
URL:            https://github.com/VictorNagibator/pg_integrity_checksums
Source0:        %{sname}-%{version}.tar.gz
# Normalized with GNU tar from https://api.github.com/repos/VictorNagibator/pg_integrity_checksums/tarball/v2.0.0
# SHA256: 73297f1433538c31a2edc8953c0a024f401d3718121286fe683601a960bf8f13

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Compute physical and logical checksums for pages, cells, rows, tables,
indexes and databases. This is the renamed continuation of the SQL extension
pg_checksums, unrelated to the PostgreSQL and PGDG command-line utilities.
Follow upstream MIGRATION.md when moving from the old extension name.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md Changes MIGRATION.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif
%exclude /usr/lib/.build-id

%changelog
* Wed Oct 28 2026 Ruohang Feng <rh@vonng.com> - 2.0.0-1PGSTY
- Initial RPM release for PostgreSQL 14 through 18.
- Preserve native debug information and PGXS bitcode in the main package.
