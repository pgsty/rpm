%define debug_package %{nil}
%global pname pg_ai_query
%global sname pg_ai_query
%global pginstdir /usr/pgsql-%{pgmajorversion}

# pg_ai_query is a pure CMake project, does not use PGXS
# Therefore no LLVM bitcode is generated, no llvmjit subpackage

# IMPORTANT: This extension requires:
#   - C++20 with <format> support (GCC 13+)
#   - OpenSSL 3.0.0+ (httplib requirement)
# Therefore: Only EL9+ is supported. EL8 cannot build this extension.

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.1
Release:	1PIGSTY%{?dist}
Summary:	AI-powered SQL query generation for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/benodiwal/pg_ai_query
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/benodiwal/pg_ai_query/archive/refs/tags/v0.1.1.tar.gz
#           Supported: PostgreSQL 14, 15, 16, 17, 18
#           Note: Source tarball must include ai-sdk-cpp submodule

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cmake >= 3.16
BuildRequires:	openssl-devel >= 3.0.0
BuildRequires:	libcurl-devel

# GCC 13+ required for C++20 <format> header support
%if 0%{?rhel} == 9
BuildRequires:	gcc-toolset-13-gcc-c++
%else
BuildRequires:	gcc-c++ >= 13
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	openssl >= 3.0.0
Requires:	libcurl

%description
pg_ai_query is a PostgreSQL extension that leverages AI to convert natural
language descriptions into SQL queries. It integrates with OpenAI, Anthropic,
and Google Gemini APIs.

Features:
- Natural language to SQL conversion with automatic schema discovery
- Query performance analysis using EXPLAIN ANALYZE with AI-powered insights
- Multiple response formats: plain SQL, annotated explanations, or JSON
- Safety protections against system table access and dangerous operations
- Flexible configuration supporting multiple AI providers

%prep
%setup -q -n %{sname}-%{version}

%build
export PATH=%{pginstdir}/bin:$PATH

# Enable GCC Toolset 13 on EL9 for C++20 <format> support
%if 0%{?rhel} == 9
source /opt/rh/gcc-toolset-13/enable
export CC=/opt/rh/gcc-toolset-13/root/usr/bin/gcc
export CXX=/opt/rh/gcc-toolset-13/root/usr/bin/g++
%endif

# Create build directory and configure with CMake
# CMake will auto-detect PostgreSQL via pg_config in PATH
# CMake will auto-set C++20 standard as required
mkdir -p build
cd build
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=${CC:-gcc} \
    -DCMAKE_CXX_COMPILER=${CXX:-g++}

# Build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin:$PATH

cd build
%{__make} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*
# Exclude ai-sdk-cpp and its dependencies (zlib, nlohmann_json) installed by CMake
%exclude /usr/local/*

%changelog
* Mon Dec 16 2024 Vonng <rh@vonng.com> - 0.1.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
