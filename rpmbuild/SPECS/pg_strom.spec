%define debug_package %{nil}
%global _build_id_links none
%global sname pg_strom
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global cuda_version 13.1
%global cuda_path /usr/local/cuda-%{cuda_version}
%global systemd_conf %{_sysconfdir}/systemd/system/postgresql-%{pgmajorversion}.service.d/%{sname}.conf
%global source_commit 374b1501e3b6b258fc4db27bd043179660a4b340
%global source_sha256 48c7d15be97719d97e0506408acc919bd16a3b06df4d2811d1d825e2c5590491

%if 0%{?rhel} != 10
%{error:pg_strom 3.5 in this spec is the EL10 compatibility build}
%endif

%if 0%{?pgmajorversion} != 14
%{error:pg_strom 3.5 in this spec only supports PostgreSQL 14}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        3.5
Release:        1PIGSTY%{?dist}
Summary:        GPU-accelerated SQL execution for PostgreSQL 14
License:        PostgreSQL
URL:            https://github.com/heterodb/pg-strom
Source0:        https://github.com/heterodb/pg-strom/archive/refs/tags/v%{version}.tar.gz
Patch0:         %{sname}-%{version}-cuda13-el10.patch
ExclusiveArch:  x86_64

BuildRequires:  gcc make patch binutils
BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  pgdg-srpm-macros >= 1.0.27
BuildRequires:  cuda-nvcc-13-1 >= %{cuda_version}
BuildRequires:  cuda-cuobjdump-13-1 >= %{cuda_version}
BuildRequires:  cuda-cudart-devel-13-1 >= %{cuda_version}
BuildRequires:  cuda-driver-devel-13-1 >= %{cuda_version}
BuildRequires:  cuda-nvrtc-devel-13-1 >= %{cuda_version}
BuildRequires:  cuda-nvml-devel-13-1 >= %{cuda_version}
BuildRequires:  nvidia-driver-cuda-libs
Requires:       postgresql%{pgmajorversion}-server
Requires:       cuda-13-1 >= %{cuda_version}
Requires:       nvidia-driver-cuda-libs
Requires:       /sbin/ldconfig
Requires(post): glibc
Requires(postun): glibc

Obsoletes:      nvme_strom < 2.0
Obsoletes:      %{sname}-%{pgmajorversion} < 2.3-2

%description
PG-Strom accelerates PostgreSQL analytical queries with NVIDIA GPUs. This
package ports the last PostgreSQL 14 compatible upstream release to EL10 and
CUDA 13.1. CUDA 13 supports Turing (compute capability 7.5) and newer targets.

%package test
Summary:        PG-Strom test data generator
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
This package provides the Star Schema Benchmark data generator shipped with
PG-Strom.

%prep
test "$(sha256sum %{SOURCE0} | awk '{print $1}')" = "%{source_sha256}"
%autosetup -p1 -n pg-strom-%{version}

%build
%{__make} %{?_smp_mflags} \
    CUDA_PATH=%{cuda_path} \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    PGSTROM_GITHASH=%{source_commit}

%install
%{__rm} -rf %{buildroot}
%{__make} install \
    CUDA_PATH=%{cuda_path} \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    PGSTROM_GITHASH=%{source_commit} \
    DESTDIR=%{buildroot}
%{__install} -Dpm 0644 files/systemd-pg_strom.conf \
    %{buildroot}%{systemd_conf}

%check
test -s pg_strom.so
test -x utils/gpuinfo
test -x utils/dbgen-ssbm
test -s src/cuda_common.fatbin
test -s src/cuda_common.gfatbin
%{cuda_path}/bin/cuobjdump --list-ptx src/cuda_common.fatbin | grep -q 'PTX file'
%{cuda_path}/bin/cuobjdump --list-elf src/cuda_common.fatbin | grep -q 'sm_86'
grep -q '^PGSTROM_VERSION := 3.5$' Makefile
readelf -d pg_strom.so | grep -q 'Shared library: \[libcuda.so.1\]'
readelf -Ws pg_strom.so | grep -q 'cuCtxCreate_v2'
readelf -Ws pg_strom.so | grep -q 'cuMemPrefetchAsync_ptsz'
readelf -d utils/gpuinfo | grep -q 'Shared library: \[libnvidia-ml.so.1\]'

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/bin/gpuinfo
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/*
%config(noreplace) %{systemd_conf}
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/src/*.bc

%files test
%{pginstdir}/bin/dbgen-ssbm

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 3.5-1PIGSTY
- Port PostgreSQL 14 build to EL10 with CUDA 13.1 compatibility
- Use CUDA legacy ABI entry points retained by the CUDA 13 driver
- Compile fatbins for Turing, Ampere, and forward-compatible PTX
