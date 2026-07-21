%global sname ivorysql-18-contrib
%global ivoryversion 5.4
%global pgmajorversion 18
%global pgbaseinstdir /usr/ivory-18

# PostgreSQL modules export extension entry points. They are private to the
# IvorySQL server ABI and must not become system-wide ELF providers.
%global __provides_exclude_from ^%{pgbaseinstdir}/lib/postgresql/.*\\.so.*$

%define debug_package %{nil}
%define _build_id_links none

Name:           %{sname}
Version:        %{ivoryversion}
Release:        2PIGSTY%{?dist}
Summary:        External extensions for IvorySQL 5 / PostgreSQL 18
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND GPL-2.0-or-later AND MIT AND PostgreSQL
URL:            https://github.com/IvorySQL/IvorySQL
Source0:        %{sname}-%{version}-sources.tar.gz
Source1:        ivorysql-contrib-build.sh
Source2:        ivorysql-18-contrib-extensions.md
Source3:        sfcgal-config-pkgconf

ExclusiveArch:  aarch64 x86_64

BuildRequires:  ivorysql-18 >= 5.0
BuildRequires:  ivorysql-18 < 6.0
BuildRequires:  autoconf automake bison boost-devel cmake flex gcc gcc-c++ git
BuildRequires:  libtool make pkgconf-pkg-config
%if 0%{?rhel} == 8
# IvorySQL's EL8 PL/Perl module links Perl 5.26. Request the matching module
# packages instead of DNF's newest Perl 5.32 modular stream. FindBin is part
# of perl-interpreter on EL8 and must not pull the incompatible split package.
BuildRequires:  perl-interpreter < 4:5.30
BuildRequires:  perl-version = 6:0.99.24-1.el8
%else
BuildRequires:  perl-interpreter
BuildRequires:  perl(version)
%endif
BuildRequires:  clang llvm-devel
BuildRequires:  SFCGAL-devel geos314-devel
%if 0%{?rhel} == 8
BuildRequires:  gdal38-devel proj96-devel
%else
BuildRequires:  gdal311-devel proj97-devel
%endif
BuildRequires:  gmp-devel json-c-devel libgeotiff17-devel libxml2-devel libxslt-devel
BuildRequires:  pcre2-devel protobuf-c-devel xerces-c-devel
BuildRequires:  groonga-devel >= 15.1.7
BuildRequires:  hiredis-devel libcurl-devel msgpack-devel scws xxhash-devel

Requires:       ivorysql-18%{?_isa} >= 5.0
Requires:       ivorysql-18%{?_isa} < 6.0
Requires:       python3-psycopg2

%description
External extensions compiled against the IvorySQL 5 / PostgreSQL 18 ABI and
installed below %{pgbaseinstdir}. This package fills the complete extension
gap between Pigsty's ivorysql-18 kernel RPM and the official IvorySQL 5.4
bundle: 29 extension controls from 23 projects, plus the wal2json output
plugin. Non-PostgreSQL runtime libraries remain normal RPM dependencies.

%prep
%setup -q -n %{sname}-%{version}-sources
%{__cp} -p %{SOURCE1} ivorysql-contrib-build.sh
%{__cp} -p %{SOURCE2} EXTENSIONS.md
%{__cp} -p %{SOURCE3} sfcgal-config-pkgconf
%{__chmod} +x ivorysql-contrib-build.sh sfcgal-config-pkgconf

%build
RPM_BUILD_NCPUS=%{_smp_build_ncpus} ./ivorysql-contrib-build.sh

%install
%{__mkdir_p} %{buildroot}
%{__cp} -a stage/usr %{buildroot}/
# pg_partman's maintenance tools are Python 3 programs. EL rejects the
# ambiguous legacy /usr/bin/env python shebang.
find %{buildroot}%{pgbaseinstdir}/bin -maxdepth 1 -type f -name '*.py' \
    -exec sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/python3|' {} +

%check
test "$(find %{buildroot}%{pgbaseinstdir}/share/postgresql/extension -maxdepth 1 -name '*.control' | wc -l)" -eq 29
test "$(find %{buildroot}%{pgbaseinstdir}/lib/postgresql -maxdepth 1 -type f -name '*.so' | wc -l)" -eq 31
test -f %{buildroot}%{pgbaseinstdir}/lib/postgresql/wal2json.so
grep -Eq "^default_version[[:space:]]*=[[:space:]]*'?2[.]8'?" \
  %{buildroot}%{pgbaseinstdir}/share/postgresql/extension/plpgsql_check.control

%files
%doc EXTENSIONS.md SOURCES.sha256 FILES.sha256
%{pgbaseinstdir}

%changelog
* Mon Jul 20 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 5.4-2PIGSTY
- Build all 23 upstream projects from source on each target OS and architecture
- Require the IvorySQL 5.x ABI range instead of one exact kernel release
- Pin plpgsql_check to the official 2.8 ABI for official-database compatibility
- Select the PGDG GDAL and PROJ development stacks appropriate for EL8 or EL9+

* Mon Jul 20 2026 Ruohang Feng (Vonng) <rh@vonng.com> - 5.4-1PIGSTY
- Add all 29 extensions missing from Pigsty's IvorySQL 5.4 kernel package
- Add wal2json and the complete PostGIS, pgRouting, PGroonga, and FTS payloads
- Reuse EL system libraries instead of embedding private dependency copies
