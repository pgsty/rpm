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
Version:        1.0.1
Release:        1PGSTY%{?dist}
Summary:        Multilingual full-text search with ICU segmentation and normalization
License:        PostgreSQL
URL:            https://github.com/benjaminsanborn/textsearch_intl
Source0:        textsearch_intl-%{version}.tar.gz
# https://codeload.github.com/benjaminsanborn/textsearch_intl/tar.gz/refs/tags/v1.0.1
# SHA256: 97c7843fd2e5d6f266ae961dc879d148dc3959c0daf75370c192d5b6189a0269

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
and the unaccent extension. The upstream SQL extension version remains 1.0.

%prep
%setup -q -n textsearch_intl-%{version}

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
* Fri Oct 23 2026 Ruohang Feng <rh@vonng.com> - 1.0.1-1PGSTY
- Update to 1.0.1, fixing tokens that normalize to an empty lexeme.
- Preserve the upstream SQL extension version 1.0.

* Thu Oct 15 2026 Ruohang Feng <rh@vonng.com> - 1.0.0-1PGSTY
- Initial package for PostgreSQL 14 through 18.
- Pin the unreleased textsearch_intl rename at commit 3cc6bf9.
