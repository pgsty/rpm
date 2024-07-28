%define debug_package %{nil}
Name:           libduckdb
Version:        1.0.0
Release:        1PIGSTY%{?dist}
Summary:        In-process SQL OLAP Database Management System
License:        MIT License
URL:            https://github.com/duckdb/duckdb/
Source0:        https://github.com/duckdb/duckdb/releases/download/v%{version}/libduckdb-%{version}.tar.gz
# https://github.com/duckdb/duckdb/releases/download/v1.0.0/libduckdb-src.zip

%description
DuckDB is a high-performance analytical database system.
It is designed to be fast, reliable, portable, and easy to use.
DuckDB provides a rich SQL dialect, with support far beyond basic SQL.
DuckDB supports arbitrary and nested correlated subqueries, window functions,
collations, complex types (arrays, structs), and more.

%prep
%setup -q -n libduckdb-%{version}

%build
clang++ -c -fPIC -std=c++11 -D_GLIBCXX_USE_CXX11_ABI=0 duckdb.cpp -o duckdb.o
clang++ -shared -o libduckdb.so *.o

%install
mkdir -p %{buildroot}/usr/lib64
install -m 0755 libduckdb.so %{buildroot}/usr/lib64

%files
/usr/lib64/libduckdb.so

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Fri Jun 28 2024 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 0.10.2-1PIGSTY
* Tue Jan 30 2024 Vonng <rh@vonng.com> - 0.9.2-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>