%global pname pg_tre
%global sname pg_tre
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 17 || 0%{?pgmajorversion} > 18
%{error:pg_tre is packaged for PostgreSQL 17 and 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        4.5.2
Release:        1PGSTY%{?dist}
Summary:        Native index access method for approximate regular expressions
License:        MIT AND BSD-2-Clause
URL:            https://codeberg.org/gregburd/pg_tre
Source0:        %{sname}-%{version}.tar.gz
# Complete upstream release archive, including the pinned TRE and Lime sources:
# https://github.com/gburd/pg_tre/releases/download/v4.5.2/pg_tre-4.5.2.tar.gz
Patch0:         pg-tre-4.5.2-build-flags.patch

BuildRequires:  gcc make git autoconf automake libtool gettext-devel m4
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server
Provides:       bundled(tre) = 0.9.0

%description
pg_tre provides a native text index access method for approximate regular
expression matching, backed by compressed trigram postings and the TRE
matcher. It also supports regular expressions, LIKE and edit-distance
ordering. Version 4.5.2 uses generic WAL and needs no shared preload.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1
cp vendor/tre/LICENSE LICENSE.tre
sed -n '1,/^ \*\//p' include/pg_tre/sparsemap.h > LICENSE.sparsemap

%build
%set_build_flags
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
    PG_CFLAGS="%{build_cflags}" PG_LDFLAGS="%{build_ldflags}"

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE LICENSE.tre LICENSE.sparsemap NOTICE
%doc README.md CHANGELOG.md LIMITATIONS.md doc/pg_tre.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Sat Oct 24 2026 Ruohang Feng <rh@vonng.com> - 4.5.2-1PGSTY
- Update to upstream 4.5.2 with newline-anchor and release archive fixes.

* Fri Oct 23 2026 Vonng <rh@vonng.com> - 4.5.1-1PGSTY
- Initial RPM release for PostgreSQL 17 and 18
- Honor build flags for vendored components and preserve debug information
- Include PGXS bitcode in the main package
