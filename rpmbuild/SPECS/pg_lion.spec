%global pname pg_lion
%global sname pg_lion
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_lion supports PostgreSQL 16 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.3.0
Release:        1PGSTY%{?dist}
Summary:        Roaring bitmap inverted indexes for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/cgkanchi/pg_lion
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/cgkanchi/pg_lion/archive/refs/tags/v0.3.0.tar.gz

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
pg_lion provides roaring bitmap inverted indexes for filtering, counting,
grouping, arrays, JSONB and full-text search. The package also includes
pg_lion_citext and pg_lion_vector. These optional companions require citext
and pgvector 0.7 or later, respectively, when created in a database.
Preloading pg_lion is optional and enables its custom WAL resource manager.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md docs/GUIDE.md docs/REFERENCE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}*.control
%{pginstdir}/share/extension/%{pname}*--*.sql
%exclude /usr/lib/.build-id/*
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Fri Nov 06 2026 Vonng <rh@vonng.com> - 0.3.0-1PGSTY
- Initial package for PostgreSQL 16 through 18
- Include the citext and pgvector companion extensions
