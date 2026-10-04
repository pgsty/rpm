%global pname pgexporter_ext
%global sname pgexporter_ext
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgexporter_ext only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.2.5
Release:        1PGSTY%{?dist}
Summary:        Operating system metrics for PostgreSQL
License:        BSD-3-Clause
URL:            https://github.com/pgexporter/pgexporter_ext
Source0:        pgexporter_ext-0.2.5.tar.gz
# Source: https://codeload.github.com/pgexporter/pgexporter_ext/tar.gz/0.2.5
# SHA256: f22af4223814858d61892037daa81ff85105fa9ac95c2c6082981c15ff76904e

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  cmake openssl-devel
Requires:       postgresql%{pgmajorversion}-server

%description
Operating system metrics for PostgreSQL.

%prep
%setup -q -n pgexporter_ext-0.2.5

%build
%set_build_flags
export PATH=%{pginstdir}/bin:$PATH
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_SKIP_RPATH=ON
cmake --build build %{?_smp_mflags}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so*
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 0.2.5-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
