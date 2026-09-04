%global sname pg_datasentinel
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 15
%{error:pg_datasentinel only supports PostgreSQL 15+}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1PGSTY%{?dist}
Summary:	Observability and activity monitoring extension for PostgreSQL
License:	BSD-3-Clause
URL:		https://github.com/datasentinel/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_datasentinel is a PostgreSQL observability extension that extends
pg_stat_activity with per-backend memory and temporary file usage, captures
vacuum, analyze, temporary file, and checkpoint activity into shared-memory
ring buffers, and reports wraparound risk and container resource limits.
It must be loaded through shared_preload_libraries.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc
%{pginstdir}/lib/bitcode/%{sname}/*/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Restrict builds to PostgreSQL 15+ to match upstream support and DEB pgversions
- Initial RPM release
- https://github.com/datasentinel/pg_datasentinel/tree/1.0
