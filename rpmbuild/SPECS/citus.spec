%define debug_package %{nil}
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global _build_id_links none
%global sname citus

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension that transforms Postgres into a distributed database
Name:		%{sname}_%{pgmajorversion}
Version:	14.0.0
Release:	1PIGSTY%{dist}
License:	AGPL-3.0
URL:		https://github.com/citusdata/%{sname}
Source0:    https://repo.pigsty.cc/ext/%{sname}-%{version}.tar.gz
#Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
BuildRequires:	libxslt-devel openssl-devel pam-devel readline-devel
BuildRequires:	libcurl-devel pgdg-srpm-macros libzstd-devel krb5-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Citus horizontally scales PostgreSQL across commodity servers
using sharding and replication. Its query engine parallelizes
incoming SQL queries across these servers to enable real-time
responses on large datasets.

Citus extends the underlying database rather than forking it,
which gives developers and enterprises the power and familiarity
of a traditional relational database. As an extension, Citus
supports new PostgreSQL releases, allowing users to benefit from
new features while maintaining compatibility with existing
PostgreSQL tools. Note that Citus supports many (but not all) SQL
commands.

%package devel
Summary:	Citus development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes development libraries for Citus.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for citus
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for citus
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%configure PG_CONFIG=%{pginstdir}/bin/pg_config
make %{?_smp_mflags}

%install
%make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/%{sname}_columnar.so
%{pginstdir}/lib/%{sname}_pgoutput.so
%{pginstdir}/lib/%{sname}_wal2json.so
%dir %{pginstdir}/lib/%{sname}_decoders/
%{pginstdir}/lib/%{sname}_decoders/pgoutput.so
%{pginstdir}/lib/%{sname}_decoders/wal2json.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_columnar-*.sql
%{pginstdir}/share/extension/columnar-*.sql
%{pginstdir}/share/extension/%{sname}_columnar.control

%files devel
%defattr(-,root,root,-)
%{pginstdir}/include/server/citus_version.h
%{pginstdir}/include/server/distributed/*.h

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*/*.bc
    %{pginstdir}/lib/bitcode/%{sname}_columnar/*
    %{pginstdir}/lib/bitcode/%{sname}_pgoutput/*
    %{pginstdir}/lib/bitcode/%{sname}_wal2json/*
%endif

%changelog
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 14.0.0-1PIGSTY
* Tue Nov 11 2025 Vonng <rh@vonng.com> - 13.2.0-8PIGSTY
* Tue Jun 24 2025 Vonng <rh@vonng.com> - 13.1.0-9PIGSTY
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 13.0.3-9PIGSTY
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 13.0.2-9PIGSTY
- https://github.com/citusdata/citus/blob/release-13.0/CHANGELOG.md
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 13.0.1-9PIGSTY
- Bump to 13.0.1 and drop PostgreSQL 14 support
* Thu Jan 23 2025 Vonng <rh@vonng.com> - 13.0.0-9PIGSTY
- Bump to 13.0.0 with PostgreSQL 17 support
* Tue Dec 24 2024 Vonng <rh@vonng.com> - 12.1.6-9PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
