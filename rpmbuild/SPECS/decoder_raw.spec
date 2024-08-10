%global pname decoder_raw
%global sname decoder_raw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1PIGSTY%{?dist}
Summary:	Output plugin for logical replication in Raw SQL format
License:	PostgreSQL
URL:		https://github.com/michaelpq/pg_plugins/blob/main/decoder_raw/
Source0:	decoder_raw-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
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

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>