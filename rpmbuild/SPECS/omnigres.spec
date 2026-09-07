%global pname omnigres
%global sname omnigres
%global pginstdir /usr/pgsql-%{pgmajorversion}
%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgmajorversion must be one of 14, 15, 16, 17, or 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	20260212
Release:	1PGSTY%{?dist}
Summary:	Postgres as a Platform
License:	Apache-2.0
URL:		https://github.com/omnigres/omnigres
Source0:	omnigres-%{version}.tar.gz
Patch0:		omnigres-20260212.patch
Patch1:		omnigres-el8-compat.patch
BuildRequires:	pgdg-srpm-macros >= 1.0.27 cmake flex bison nmap-ncat make
BuildRequires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}-contrib postgresql%{pgmajorversion}-plpython3
%if 0%{?rhel} == 8
BuildRequires:	python3.12-devel
%global omnigres_python /usr/bin/python3.12
%else
BuildRequires:	python3-devel
%global omnigres_python /usr/bin/python3
%endif
%if 0%{?rhel} < 10
BuildRequires:	gcc-toolset-15-gcc gcc-toolset-15-gcc-c++
%endif
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib postgresql%{pgmajorversion}-plpython3 python3-pip

%description
Omnigres makes Postgres a developer-first application platform.
You can deploy a single database instance and it can host your entire application, scaling as needed.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1 -F0
%if 0%{?rhel} == 8
%patch -P 1 -p1
%endif

%build
%set_build_flags
%if 0%{?rhel} < 10
source /opt/rh/gcc-toolset-15/enable
%endif
cmake -S . -B pg%{pgmajorversion} -DCMAKE_BUILD_TYPE=Release -DOPENSSL_CONFIGURED=1 -DPython3_EXECUTABLE=%{omnigres_python} -DPG_CONFIG=/usr/pgsql-%{pgmajorversion}/bin/pg_config
cmake --build pg%{pgmajorversion} --parallel --target inja
cmake --build pg%{pgmajorversion} --parallel --target package_extensions

%install
rm -rf %{buildroot}
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
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 20260212-1PGSTY
- Update to the 2026-02-12 upstream snapshot
- Preserve and migrate omni_httpc 0.1.10 installations safely
- Gate the unsafe HTTP/3 path with a feature-not-supported error

* Wed Jul 22 2026 Vonng <rh@vonng.com> - 20251108-2PIGSTY
- Build with current GCC toolsets and validate packaged extension payload
- Add EL8 compatibility for OpenSSL and gettid APIs

* Sat Nov 08 2025 Vonng <rh@vonng.com> - 20251108-1PIGSTY
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 20251025-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 20250507-1PIGSTY
* Mon Jan 20 2025 Vonng <rh@vonng.com> - 20250120-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
