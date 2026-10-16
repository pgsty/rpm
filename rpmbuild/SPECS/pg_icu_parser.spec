%global pname pg_icu_parser
%global sname pg_icu_parser
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_icu_parser is packaged for PostgreSQL 14 through 18}
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
Summary:        PostgreSQL text search parser using ICU boundary analysis
License:        MPL-2.0
URL:            https://github.com/IgKh/pg_icu_parser
Source0:        pg_icu_parser-1.0.0.tar.gz
# https://codeload.github.com/IgKh/pg_icu_parser/tar.gz/v1.0.0
# SHA256: 6fdccc5dce2274257556a6e96139cc6ab0f7c4deee5ac7fc28e1a14fc16f7b10

Patch0:         pg_icu_parser-1.0.0-pg18-icu.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc libicu-devel pkgconfig
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pg_icu_parser provides the icu_parser text search parser using ICU word
boundary analysis. It supports multilingual tokenization and a configurable
ICU locale. The ts_headline function is not supported.

%prep
%setup -q -n pg_icu_parser-1.0.0
%patch0 -p1

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
- Use public encoding APIs on PG18 and link ICU explicitly.
