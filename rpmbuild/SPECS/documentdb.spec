%global pname documentdb
%global sname documentdb
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
Version:	0.104
Release:	0PIGSTY%{?dist}
Summary:	Native implementation of document-oriented NoSQL database on PostgreSQL
License:	MIT
URL:		https://github.com/FerretDB/documentdb
Source0:	%{sname}-%{version}.0-ferretdb-2.3.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:   postgresql%{pgmajorversion}-contrib
Requires:   pg_cron_%{pgmajorversion}
Requires:   pgvector_%{pgmajorversion}
Requires:   rum_%{pgmajorversion}
Recommends: postgis35_%{pgmajorversion}

# Require extra dependencies for building: https://github.com/microsoft/documentdb/tree/main/scripts
# Available for PostgreSQL 15,16,17

%description
DocumentDB offers a native implementation of document-oriented NoSQL database,
enabling seamless CRUD operations on BSON data types within a PostgreSQL framework.
Beyond basic operations, DocumentDB empowers you to execute complex workloads,
including full-text searches, geospatial queries, and vector embeddings on your dataset,
delivering robust functionality and flexibility for diverse data management needs.

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
%setup -q -n %{pname}-%{version}.0-ferretdb-2.3.0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}
cd pg_documentdb_core
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
cd pg_documentdb_core
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/pg_%{pname}*.so
%{pginstdir}/share/extension/%{pname}*.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Fri Jul 04 2025 Vonng <rh@vonng.com> - 0.104-0PIGSTY
- add lots of new features
* Thu May 22 2025 Vonng <rh@vonng.com> - 0.103-0PIGSTY
- add pg_documentdb_gw and arm64 support
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.102-0PIGSTY
- FerretDB modified version: https://github.com/FerretDB/documentdb
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.101-0PIGSTY
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 0.100-0PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>