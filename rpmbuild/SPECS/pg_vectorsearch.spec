%global pname pg_vectorsearch
%global sname pg_vectorsearch
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_vectorsearch currently supports PostgreSQL 18 only}
%endif

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg with_llvm=yes
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        Approximate nearest neighbor search with the PRISM index
License:        PostgreSQL
URL:            https://github.com/timescale/pg_vectorsearch
Source0:        https://github.com/timescale/pg_vectorsearch/releases/download/v%{version}/%{sname}-%{version}.tar.gz
Patch0:         pg_vectorsearch-0.1.0-rpath.patch
Patch1:         pg_vectorsearch-0.1.0-clang15-atomics.patch
Patch2:         pg_vectorsearch-0.1.0-llvm15-ifunc.patch

%if 0%{?rhel} == 8
# EL8 ships GCC 8 and Meson 0.58. Use a supported compiler and a pinned,
# build-only Meson source; neither tool enters the extension payload.
Source1:        https://github.com/mesonbuild/meson/releases/download/0.63.3/meson-0.63.3.tar.gz
BuildRequires:  gcc-toolset-13-gcc
BuildRequires:  gcc-toolset-13-gcc-plugin-annobin
BuildRequires:  python3.11
%global pgvs_meson /usr/bin/python3.11 meson-0.63.3/meson.py
%else
BuildRequires:  gcc >= 11
BuildRequires:  meson >= 0.61
%global pgvs_meson meson
%endif
BuildRequires:  make
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  pkgconfig(openblas)
BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
pg_vectorsearch provides the PRISM approximate nearest neighbor index with
RaBitQ quantization, SIMD distance kernels, and native vec32/vec16 types.
It can also index existing pgvector vector/halfvec columns without requiring
pgvector for standalone use. This upstream alpha release is for evaluation.

%prep
%if 0%{?rhel} == 8
%setup -q -n %{sname}-%{version} -a 1
%else
%setup -q -n %{sname}-%{version}
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%set_build_flags
%if 0%{?rhel} == 8
source /opt/rh/gcc-toolset-13/enable
%endif
%{pgvs_meson} setup builddir --buildtype=release -Dstrip=false \
    -Dpostgresql=enabled -Dpg_config=%{pginstdir}/bin/pg_config \
    -Dnative=false -Dsimd=full -Dblas=enabled \
    -Dtools=disabled -Dhdf5=disabled -Dfaiss=false
%{pgvs_meson} compile -C builddir -j %{_smp_build_ncpus}

# Upstream Meson does not emit PostgreSQL JIT bitcode. Reuse PGXS's Clang
# rules and thin-link installer for exactly the sources in the native module.
# Meson's target manifest also selects the correct architecture's SIMD files.
python3 - <<'PY'
import json
from pathlib import Path

root = Path.cwd()
module = 'pg_vectorsearch-' + (root / 'VERSION').read_text().strip()
targets = json.loads((root / 'builddir/meson-info/intro-targets.json').read_text())
selected = [target for target in targets if target['name'] in ('vs_pg', module)]
assert len(selected) == 2, 'expected the PostgreSQL core library and extension'
sources = sorted({
    str(Path(source).resolve().relative_to(root))
    for target in selected
    for group in target['target_sources']
    for source in group.get('sources', [])
    if source.endswith('.c')
})
assert sources and all(source.startswith('src/') for source in sources)
objects = ' '.join(str(Path(source).with_suffix('.o')) for source in sources)
makefile = '''MODULE_big = {module}
OBJS = {objects}
PG_CPPFLAGS = -I$(CURDIR)/src -I$(CURDIR)/src/pg -I$(CURDIR)/builddir -DVS_DISABLE_IFUNC
PG_CPPFLAGS += -std=gnu11 -ffp-contract=fast -fassociative-math -fno-signed-zeros -fno-trapping-math
PG_CPPFLAGS += $(shell pkg-config --cflags openblas)
PG_CONFIG ?= pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
# LLVM 15 cannot thin-link x86 target_clones IFUNC summaries.
# Keep all modules and native SIMD; only JIT bitcode uses the generic clones.
ifeq ($(shell $(CLANG) -dumpversion | cut -d. -f1),15)
BITCODE_CFLAGS += -DVS_DISABLE_TARGET_CLONES
endif
.PHONY: bitcode install-bitcode
ifeq ($(with_llvm),yes)
bitcode: $(OBJS:.o=.bc)
install-bitcode: bitcode
\t$(call install_llvm_module,$(MODULE_big),$(OBJS))
else
bitcode install-bitcode:
endif
'''
(root / 'Makefile.llvm').write_text(makefile.format(module=module, objects=objects))
PY
%{__make} -f Makefile.llvm bitcode %{?_smp_mflags} \
    PG_CONFIG=%{pginstdir}/bin/pg_config LLVM_BINPATH=/usr/bin %{with_llvm_arg}

%install
DESTDIR=%{buildroot} %{pgvs_meson} install -C builddir --no-rebuild
# The regression helper is test-only and must never enter the runtime RPM.
%{__rm} -f %{buildroot}%{pginstdir}/lib/pgvs_test_helpers.so
# find-debuginfo scans executable ELF files; the packaged library remains 0644.
chmod 0755 %{buildroot}%{pginstdir}/lib/%{pname}-%{version}.so
%{__make} -f Makefile.llvm install-bitcode \
    PG_CONFIG=%{pginstdir}/bin/pg_config LLVM_BINPATH=/usr/bin \
    DESTDIR=%{buildroot} %{with_llvm_arg}

%files
%license LICENSE
%doc README.md CHANGELOG.md docs/tuning.md docs/maintenance.md
%attr(0644,root,root) %{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--%{version}.control
%{pginstdir}/share/extension/%{pname}--%{version}.sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}-%{version}/
%{pginstdir}/lib/bitcode/%{pname}-%{version}.index.bc
%endif

%changelog
* Thu Oct 15 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Support EL8 with GCC Toolset 13 and pinned build-only Meson 0.63.3
- Keep atomic function pointer initialization compatible with Clang 15
- Avoid LLVM 15 IFUNC thin-link failures while retaining native SIMD and bitcode
- Package the upstream alpha release for PostgreSQL 18 evaluation
- Retain portable SIMD, OpenBLAS, DWARF, and main-package LLVM bitcode
- Exclude the regression helper library from the runtime package
- Remove the unnecessary PostgreSQL library RPATH
