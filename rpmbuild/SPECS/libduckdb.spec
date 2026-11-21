Name:           libduckdb
Version:        1.5.6
Release:        1PGSTY%{?dist}
# Official assets contain symbol tables, but no DWARF or source paths.
# Automatic debuginfo can preserve symbols only; it is not full source debugging.
%undefine _debugsource_packages
Summary:        In-process analytical database library
License:        MIT
URL:            https://github.com/duckdb/duckdb
%ifarch aarch64
Source0:        libduckdb-%{version}-arm64.tar.gz
%else
Source0:        libduckdb-%{version}-amd64.tar.gz
%endif
ExclusiveArch:  x86_64 aarch64
BuildRequires:  binutils

%description
DuckDB is a high-performance in-process analytical database system. This
package contains the official shared C/C++ runtime library.

%prep
%setup -q -c

%build
# The official release asset is prebuilt for the target architecture.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_libdir}
%{__install} -m 0755 libduckdb.so %{buildroot}%{_libdir}/libduckdb.so

%check
test -s libduckdb.so
%ifarch aarch64
readelf -h libduckdb.so | grep -E 'Machine:[[:space:]]+AArch64$'
%else
readelf -h libduckdb.so | grep -E 'Machine:[[:space:]]+Advanced Micro Devices X86-64$'
%endif
readelf -d libduckdb.so | grep -F 'Library soname: [libduckdb.so]'
nm -D --defined-only libduckdb.so | grep -F ' duckdb_library_version'

%files
%license LICENSE
%{_libdir}/libduckdb.so

%changelog
* Sat Nov 21 2026 Vonng <rh@vonng.com> - 1.5.6-1PGSTY
- Update the official amd64 and arm64 runtime assets to DuckDB 1.5.6
- Check the ELF architecture and document the upstream DWARF limitation

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.5.5-1PGSTY
- Initial Pigsty RPM package from official DuckDB 1.5.5 release assets
- Package deterministic amd64 and arm64 shared-library archives
- Keep automatic debuginfo while omitting empty debugsource for prebuilt assets
