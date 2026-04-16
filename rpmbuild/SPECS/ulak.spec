%global pname ulak
%global sname ulak
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
Version:	0.0.2
Release:	1PIGSTY%{?dist}
Summary:	Transactional outbox extension with background-worker delivery
License:	Apache-2.0
URL:		https://github.com/zeybek/ulak
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/ulak/0.0.2/ulak-0.0.2.zip
#           Built with HTTP, Kafka, MQTT, Redis, and AMQP dispatchers on EL9; upstream NATS support is left disabled because cnats packages are unavailable in the builder repos

BuildRequires:	gcc
BuildRequires:	libcurl-devel
BuildRequires:	openssl-devel
BuildRequires:	librdkafka-devel
BuildRequires:	mosquitto-devel
BuildRequires:	hiredis-devel
BuildRequires:	librabbitmq-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
ulak implements the transactional outbox pattern inside PostgreSQL, committing
messages atomically with business transactions and delivering them
asynchronously from background workers. This package enables the HTTP, Kafka,
MQTT, Redis Streams, and AMQP dispatchers on EL builders; upstream NATS support
remains disabled until cnats development packages are available in the build
environment.

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
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/ulak-0.0.2.patch

%build
PATH=%{pginstdir}/bin:$PATH %{__make} ENABLE_KAFKA=1 ENABLE_MQTT=1 ENABLE_REDIS=1 ENABLE_AMQP=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} ENABLE_KAFKA=1 ENABLE_MQTT=1 ENABLE_REDIS=1 ENABLE_AMQP=1 install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/doc/extension/README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Thu Apr 16 2026 Vonng <rh@vonng.com> - 0.0.2-1PIGSTY
- Initial RPM release from the official PGXN 0.0.2 source bundle
- Build the HTTP, Kafka, MQTT, Redis, and AMQP dispatchers on EL9; leave NATS disabled until cnats packages are available
- Fall back to the legacy hiredis keepalive helper on EL9's 1.0.x headers
