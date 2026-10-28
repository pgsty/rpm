%global pname oai_fdw
%global sname oai_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:oai_fdw is packaged for PostgreSQL 14 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.16.0
Release:        1PGSTY%{?dist}
Summary:        OAI-PMH foreign data wrapper for PostgreSQL
License:        MIT
URL:            https://github.com/jimjonesbr/oai_fdw
Source0:        %{sname}-%{version}.tar.gz
# Normalized with GNU tar from https://api.github.com/repos/jimjonesbr/oai_fdw/tarball/v1.16
# SHA256: 5ef6b4d97f3f3a86586bf0ccaf0f2fbc99eb0adbc1be8b67ba63b98be57ceefb

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  libcurl-devel libxml2-devel pkgconf-pkg-config
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Read metadata from OAI-PMH repositories over HTTP or HTTPS through foreign
tables. This is a read-only wrapper using libcurl and libxml2. Distribution
version 1.16.0 uses the upstream SQL extension version 1.16.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif
%exclude /usr/lib/.build-id

%changelog
* Wed Oct 28 2026 Ruohang Feng <rh@vonng.com> - 1.16.0-1PGSTY
- Initial RPM release for PostgreSQL 14 through 18.
- Preserve native debug information and PGXS bitcode in the main package.
