%global pname pg_nanotime
%global sname pg_nanotime
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_nanotime is packaged for PostgreSQL 17 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.3.0
Release:        1PGSTY%{?dist}
Summary:        Nanosecond-precision timestamp types and clocks for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/bunko666-cloud/pg_nanotime
Source0:        %{pname}-%{version}.tar.gz
# https://api.github.com/repos/bunko666-cloud/pg_nanotime/tarball/v0.3.0
# Normalize the official tag archive root with GNU tar.

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
pg_nanotime provides nanosecond-precision timestamp and interval types,
clock functions, and monotonic clocks for PostgreSQL 17 and 18.

%prep
%setup -q -n %{pname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md docs/TECHNICAL.md docs/EXAMPLES.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Tue Oct 27 2026 Ruohang Feng <rh@vonng.com> - 0.3.0-1PGSTY
- Update pg_nanotime to 0.3.0 with range and multirange support.

* Sat Oct 24 2026 Ruohang Feng <rh@vonng.com> - 0.2.0-1PGSTY
- Initial RPM release for PostgreSQL 17 through 18.
- Include PGXS bitcode and retain debuginfo and debugsource packages.
