%global pname acdat
%global sname acdat
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:acdat supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.1
Release:        1PGSTY%{?dist}
Summary:        Compiled multi-pattern matching for PostgreSQL
License:        Apache-2.0
URL:            https://github.com/pgsty/acdat
Source0:        %{sname}-%{version}.tar.gz

BuildRequires:  gcc make pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:  clang llvm
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
acdat compiles large exact-literal dictionaries into immutable Aho-Corasick
Double-Array machines. It scans PostgreSQL text or bytea values once to test
for matches, enumerate overlapping hits, or perform deterministic replacement.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%autosetup -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md docs/CHANGELOG.md docs/BENCHMARK.md docs/PERFORMANCE.md docs/USAGE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Thu Sep 03 2026 Vonng <rh@vonng.com> - 0.1.1-1PGSTY
- Update to the formal pgsty/acdat 0.1.1 release
- Preserve the 0.1.0 to 0.1.1 extension upgrade path for PostgreSQL 14 through 18
- Follow the upstream relicensing to Apache-2.0 and refreshed documentation layout

* Sat Aug 22 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
- Build for PostgreSQL 14 through 18
