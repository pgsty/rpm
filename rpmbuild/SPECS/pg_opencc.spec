%global pname opencc
%global sname pg_opencc
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_opencc supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        OpenCC Chinese conversion for PostgreSQL
License:        Apache-2.0 AND BSD-2-Clause AND MIT
URL:            https://github.com/pgsty/pg_opencc
Source0:        https://github.com/pgsty/pg_opencc/archive/refs/tags/v%{version}.tar.gz#/%{sname}-%{version}.tar.gz

BuildRequires:  gcc gcc-c++ make cmake >= 3.12
BuildRequires:  python3 pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server
Provides:       bundled(opencc) = 1.4.2
Provides:       bundled(marisa) = 0.3.1
Provides:       bundled(darts-clone) = 0.32h
Provides:       bundled(rapidjson) = 1.1.0

%description
The opencc extension converts between Simplified Chinese, Traditional Chinese,
Taiwan and Hong Kong conventions, and Japanese Shinjitai. OpenCC 1.4.2 and
its dictionaries are embedded in the shared library, with no system OpenCC
runtime dependency. Requires a UTF8 database and uses the fixed opencc schema.

%prep
%autosetup -n %{sname}-%{version}
cp vendor/README.md VENDORED-OPENCC.md
mkdir bundled-licenses
cp vendor/opencc/LICENSE bundled-licenses/OpenCC-LICENSE
cp vendor/opencc/deps/marisa-0.3.1/COPYING.md bundled-licenses/marisa-COPYING.md
cp vendor/opencc/deps/darts-clone-0.32h/COPYING.md bundled-licenses/darts-clone-COPYING.md
cat > bundled-licenses/RapidJSON-LICENSE <<'EOF'
Copyright (C) 2015 THL A29 Limited, a Tencent company, and Milo Yip.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
EOF

%build
# CMake inherits the exported flags for the bundled static libraries.
%set_build_flags
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} \
    PG_CONFIG=%{pginstdir}/bin/pg_config CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS"

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install \
    PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot}

%files
%license LICENSE NOTICE bundled-licenses/
%doc README.md CHANGELOG.md VENDORED-OPENCC.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Fri Nov 06 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Initial release for PostgreSQL 14 through 18
- Bundle OpenCC 1.4.2 and dictionaries with complete native debug information
- Include PGXS bitcode in the main package
