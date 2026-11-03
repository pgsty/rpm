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
Version:        2.1.0
Release:        1PGSTY%{?dist}
Summary:        Physical and logical data checksums for PostgreSQL
License:        MIT
URL:            https://github.com/VictorNagibator/pg_integrity_checksums
Source0:        %{sname}-%{version}.tar.gz
# Official archive: https://github.com/VictorNagibator/pg_integrity_checksums/archive/refs/tags/v2.1.0.tar.gz
# SHA256: 33b3798123f71eda7fd48238145b650ae1c87139c5f12bec2d6fe59dbaa779c0

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
* Tue Nov 03 2026 Vonng <rh@vonng.com> - 2.1.0-1PGSTY
- Update to 2.1.0 with canonical logical checksum byte order.
- https://github.com/VictorNagibator/pg_integrity_checksums/releases/tag/v2.1.0

* Fri Oct 30 2026 Ruohang Feng <rh@vonng.com> - 2.0.2-1PGSTY
- Update to upstream 2.0.2.

* Wed Oct 28 2026 Ruohang Feng <rh@vonng.com> - 2.0.0-1PGSTY
- Initial RPM release for PostgreSQL 14 through 18.
- Preserve native debug information and PGXS bitcode in the main package.
