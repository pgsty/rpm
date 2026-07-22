%define debug_package %{nil}
%global pname omnigres
%global sname omnigres
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	20251108
Release:	2PIGSTY%{?dist}
Summary:	Postgres as a Platform
License:	Apache-2.0
URL:		https://github.com/omnigres/omnigres
Source0:	omnigres-%{version}.tar.gz
Patch0:		omnigres-toolchain-compat.patch
Patch1:		omnigres-el8-compat.patch
BuildRequires:	pgdg-srpm-macros >= 1.0.27 cmake flex bison nmap-ncat
BuildRequires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}-contrib postgresql%{pgmajorversion}-plpython3
%if 0%{?rhel} == 8
BuildRequires:	python3.12-devel
%else
BuildRequires:	python3-devel
%endif
%if 0%{?rhel} < 10
BuildRequires:	gcc-toolset-15-gcc gcc-toolset-15-gcc-c++
%endif
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib postgresql%{pgmajorversion}-plpython3

%description
Omnigres makes Postgres a developer-first application platform.
You can deploy a single database instance and it can host your entire application, scaling as needed.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
%if 0%{?rhel} == 8
%patch -P 1 -p1
%endif

%build
%if 0%{?rhel} < 10
source /opt/rh/gcc-toolset-15/enable
%endif
cmake -S . -B pg%{pgmajorversion} -DCMAKE_BUILD_TYPE=Release -DOPENSSL_CONFIGURED=1 -DPython3_EXECUTABLE=/usr/bin/python3 -DPG_CONFIG=/usr/pgsql-%{pgmajorversion}/bin/pg_config
cmake --build pg%{pgmajorversion} --parallel --target inja
cmake --build pg%{pgmajorversion} --parallel --target package_extensions

%install
rm -rf %{buildroot}
test -d pg%{pgmajorversion}/packaged/extension
test -n "$(find pg%{pgmajorversion}/packaged -maxdepth 1 -name '*.so' -print -quit)"
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a pg%{pgmajorversion}/packaged/*.so %{buildroot}%{pginstdir}/lib/
cp -a pg%{pgmajorversion}/packaged/extension/* %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql
%exclude /usr/lib/.build-id

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 20251108-2PIGSTY
- Build with current GCC toolsets and validate packaged extension payload
- Add EL8 compatibility for OpenSSL and gettid APIs

* Sat Nov 08 2025 Vonng <rh@vonng.com> - 20251108-1PIGSTY
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 20251025-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 20250507-1PIGSTY
* Mon Jan 20 2025 Vonng <rh@vonng.com> - 20250120-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
