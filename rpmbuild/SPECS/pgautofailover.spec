%global sname pg_auto_failover
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	Postgres extension and service for automated failover and high-availability
Name:		%{sname}_%{pgmajorversion}
Version:	2.2
Release:	1PGSTY%{?dist}
License:	PostgreSQL
Source0:	pg_auto_failover-%{version}.tar.gz
%if 0%{?pgmajorversion} >= 18
Patch0:		pg_auto_failover-2.2.patch
%endif
URL:		https://github.com/hapostgres/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	libselinux-devel >= 2.0.93
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	selinux-policy >= 3.9.13
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
BuildRequires:	libxml2-devel libxslt-devel pam-devel
BuildRequires:	krb5-devel readline-devel zlib-devel
%if 0%{?pgmajorversion} >= 18
BuildRequires:	numactl-devel
%endif
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib

%description
pg_auto_failover is an extension and service for PostgreSQL that monitors and
manages automated failover for a Postgres cluster. It is optimized for
simplicity and correctness and supports Postgres 10 and newer.

We set up one PostgreSQL server as a monitor node as well as a primary and
secondary node for storing data. The monitor node tracks the health of the
data nodes and implements a failover state machine. On the PostgreSQL nodes,
the pg_autoctl program runs alongside PostgreSQL and runs the necessary
commands to configure synchronous streaming replication.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?pgmajorversion} >= 18
%patch -P 0 -p1
%endif

%build
PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
PG_CONFIG=%{pginstdir}/bin/pg_config %make_install %{with_llvm_arg}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md docs/
%{pginstdir}/bin/pg_autoctl
%{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/pgautofailover.so
%{pginstdir}/share/extension/pgautofailover-*.sql
%{pginstdir}/share/extension/pgautofailover.control

%if %llvm
%{pginstdir}/lib/bitcode/pgautofailover*.bc
%{pginstdir}/lib/bitcode/pgautofailover/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 2.2-5PIGSTY
- Backport upstream PostgreSQL 18 compatibility fixes

* Thu Nov 20 2025 Devrim Gündüz <devrim@gunduz.org> - 2.2-4PGDG
- Modernise OpenSSL dependencies

* Thu Apr 3 2025 Devrim Gunduz <devrim@gunduz.org> - 2.2-1PGDG
- Update to 2.2
