%global pname decoder_raw
%global sname decoder_raw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20260728
%global snapshot_commit 2271b0d525ea8a42319b0e3e85a81d152bd3ba31
%global snapshot_short 2271b0d

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	2.git%{snapshot_date}.%{snapshot_short}PGSTY%{?dist}
Summary:	Output plugin for logical replication in Raw SQL format
License:	PostgreSQL
URL:		https://github.com/michaelpq/pg_plugins/blob/main/decoder_raw/
Source0:	%{sname}-%{version}+git%{snapshot_date}.%{snapshot_short}.tar.gz
Patch0:		decoder_raw-1.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This output plugin for logical replication generates raw queries based
on the logical changes it finds. Those queries can be consumed as they
are by any remote source.

UPDATE and DELETE queries are generated for relations using a level of
REPLICA IDENTITY sufficient to ensure that tuple selectivity is guaranteed:
- FULL, all the old tuple values are decoded from WAL all the time so
they are used for WHERE clause generation.
- DEFAULT, when relation has an index usable for selectivity like a
primary key.
- USING INDEX, because the UNIQUE index on NOT NULL values ensures
that tuples are uniquely identified.
In those cases, for DEFAULT and USING INDEX, WHERE clause is generated
with new tuple values if no columns mused by the selectivity index are
updated as server does not need to provide old tuple values. If at least
one column is updated, new tuple values are added, of course only on the
columns managing tuple selectivity.
Based on that, UPDATE and DELETE queries are not generated for the following
cases of REPLICA IDENTITY:
- NOTHING
- DEFAULT without a selectivity index

INSERT queries are generated for all relations everytime using the new
tuple values fetched from WAL.

%prep
%setup -q -n %{sname}-%{version}+git%{snapshot_date}.%{snapshot_short}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.0-2.git20260728.2271b0dPGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Package upstream main snapshot 2271b0d with TRUNCATE support
- Keep PostgreSQL 14-18 callback and tuple API compatibility
- Declare clang and llvm for PGXS bitcode generation

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 1.0-2PIGSTY
- Fix PostgreSQL 14-16 tuple buffer handling with newer toolchains

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
