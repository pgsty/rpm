%global pname textsearch_intl
%global sname textsearch_intl
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:textsearch_intl is packaged for PostgreSQL 14 through 18}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.0.0
Release:        1PGSTY%{?dist}
Summary:        Multilingual full-text search with ICU segmentation and normalization
License:        PostgreSQL
URL:            https://github.com/benjaminsanborn/textsearch_intl
Source0:        textsearch_intl-1.0.0.tar.gz
# https://codeload.github.com/benjaminsanborn/textsearch_intl/tar.gz/3cc6bf9a9c22a3946802e95ff472678bb1c2c60d
# SHA256: d30b1c7f373767510ba41fd6c9244a929f3005a96d946fb1e71fc0c0962f350e

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc libicu-devel pkgconfig
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-contrib

%description
textsearch_intl provides ICU word segmentation, Unicode normalization and
optional n-gram matching for multilingual full-text search. It requires UTF-8
and the unaccent extension. This package contains a pinned upstream snapshot.

%prep
%setup -q -n textsearch_intl-3cc6bf9a9c22a3946802e95ff472678bb1c2c60d

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Thu Oct 15 2026 Ruohang Feng <rh@vonng.com> - 1.0.0-1PGSTY
- Initial package for PostgreSQL 14 through 18.
- Pin the unreleased textsearch_intl rename at commit 3cc6bf9.
