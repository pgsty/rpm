%global pname pg_failover_slots
%global sname pg_failover_slots
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
Version:	1.2.0
Release:	1PIGSTY%{?dist}
Summary:	PG Failover Slots extension
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/pg_failover_slots
Source0:	pg_failover_slots-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PG Failover Slots is for anyone with Logical Replication Slots on
Postgres databases that are also part of a Physical Streaming Replication architecture.

Since logical replication slots are only maintained on the primary node,
 downstream subscribers don't receive any new changes from a newly promoted primary until the slot is created,
which is unsafe because the information that includes which data a subscriber has confirmed receiving and
which log data still needs to be retained for the subscriber will have been lost, resulting in an unknown gap
in data changes. PG Failover Slots makes logical replication slots usable across a physical failover using the following features:

Copies any missing replication slots from the primary to the standby
Removes any slots from the standby that aren't found on the primary
Periodically synchronizes the position of slots on the standby based on the primary
Ensures that selected standbys receive data before any of the logical slot walsenders can send data to consumers
PostgreSQL 11 or higher is required.

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
Requires:	llvm => 17.0
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
%doc README.md
%{pginstdir}/lib/%{pname}.so
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>