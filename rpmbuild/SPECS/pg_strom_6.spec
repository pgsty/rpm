%global _build_id_links none
%global sname pg_strom
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global source_commit 4d12ef415759dc48cd4c1421565e9c694b7bd3f9
%global source_sha256 8de0d311e8714bd387b10b1dc7c361228e31d8d2eb34d5a8d8a192cbda427a12
%global systemd_conf %{_sysconfdir}/systemd/system/postgresql-%{pgmajorversion}.service.d/pg_strom.conf

%if 0%{?rhel} != 9 && 0%{?rhel} != 10
%{error:PG-Strom 6.1 gap RPMs support EL9 and EL10}
%endif
%if 0%{?pgmajorversion} == 15
%global pg_floor 15.20
%elif 0%{?pgmajorversion} == 16
%global pg_floor 16.16
%elif 0%{?pgmajorversion} == 17
%global pg_floor 17.12
%elif 0%{?pgmajorversion} == 18
%global pg_floor 18.7
%else
%{error:PG-Strom 6.1 gap RPMs support PostgreSQL 15 through 18}
%endif
# Keep future rebuilds paired with the minor release that supplied the headers.
%global pg_build_ver %(if test -x %{pginstdir}/bin/pg_config; then %{pginstdir}/bin/pg_config --version | cut -d' ' -f2; else echo %{pg_floor}; fi)
%global pgxs_args PG_CONFIG=%{pginstdir}/bin/pg_config CUDA_PATH=/usr/local/cuda PGSTROM_GITHASH=%{source_commit}
%{!?llvm:%global llvm 1}
%if %llvm
%global llvm_args with_llvm=yes LLVM_BINPATH=$(/usr/bin/llvm-config --bindir) CLANG=/usr/bin/clang
%else
%global llvm_args with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        6.1
Release:        1PGSTY%{?dist}
Summary:        GPU-accelerated SQL execution for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/heterodb/pg-strom
# Original source archive from the HeteroDB 6.1-0 SRPM.
Source0:        %{sname}-%{version}.0.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  gcc gcc-c++ make binutils chrpath pkgconfig
BuildRequires:  postgresql%{pgmajorversion}-devel >= %{pg_floor}
BuildRequires:  arrow-devel = 23.0.0
BuildRequires:  parquet-devel = 23.0.0
BuildRequires:  cuda >= 13.1
BuildRequires:  nvidia-driver-cuda-libs
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server%{?_isa} >= %{pg_build_ver}
Requires:       postgresql%{pgmajorversion}-libs%{?_isa} >= %{pg_build_ver}
Requires:       apache-arrow-release >= 23.0.0
Requires:       arrow2300-libs parquet2300-libs
Requires:       cuda >= 13.1
Requires:       nvidia-driver-cuda-libs
# The GPU service invokes nvcc and its host C++ compiler on first startup.
Requires:       gcc-c++

%description
PG-Strom runs PostgreSQL scans, joins and aggregates on NVIDIA GPUs.
The package includes the device sources and the pg2arrow and arrow2csv
utilities for Apache Arrow IPC and Parquet.

%prep
echo '%{source_sha256}  %{SOURCE0}' | sha256sum -c -
%setup -q -n %{sname}-%{version}.0

%build
%set_build_flags
%make_build -C src %{pgxs_args} %{llvm_args}
%make_build -C arrow-tools PG_CONFIG=%{pginstdir}/bin/pg_config \
    CXX="%{__cxx} %{build_cxxflags} %{build_ldflags}" arrow2csv pg2arrow

%install
%make_install -C src %{pgxs_args} %{llvm_args}
%{__make} -C arrow-tools PG_CONFIG=%{pginstdir}/bin/pg_config \
    DESTDIR=%{buildroot} PREFIX=%{pginstdir} install-arrow2csv install-pg2arrow

# The module loads system libraries. The Arrow client uses this major's libpq.
chrpath --delete %{buildroot}%{pginstdir}/lib/pg_strom.so
chrpath --replace '$ORIGIN/../lib' %{buildroot}%{pginstdir}/bin/pg2arrow
install -d "$(dirname %{buildroot}%{systemd_conf})"
cat > %{buildroot}%{systemd_conf} <<'CONF'
[Service]
LimitNOFILE=65536
LimitCORE=infinity
#Environment=CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1
CONF

%check
so=%{buildroot}%{pginstdir}/lib/pg_strom.so
nm -D --undefined-only "$so" | grep ' U heap_datum_check$' >/dev/null
for lib in libcuda.so.1 libarrow.so.2300 libparquet.so.2300; do
    readelf -d "$so" | grep -F "Shared library: [$lib]" >/dev/null
done
%if %llvm
bc=%{buildroot}%{pginstdir}/lib/bitcode
for file in "$bc"/pg_strom.index.bc "$bc"/pg_strom/*.bc; do
    /usr/bin/llvm-dis "$file" -o /dev/null
done
%endif

%files
%license LICENSE
%doc README.md
%{pginstdir}/bin/arrow2csv
%{pginstdir}/bin/pg2arrow
%{pginstdir}/lib/pg_strom.so
%{pginstdir}/share/extension/pg_strom.control
%{pginstdir}/share/pg_strom/
%config(noreplace) %{systemd_conf}
%if %llvm
%{pginstdir}/lib/bitcode/pg_strom.index.bc
%{pginstdir}/lib/bitcode/pg_strom/
%endif

%changelog
* Wed Nov 25 2026 Vonng <rh@vonng.com> - 6.1-1PGSTY
- Build PG15–18 gap RPMs with current PostgreSQL headers and Arrow 23.0.0
