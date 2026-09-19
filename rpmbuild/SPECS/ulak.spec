%global pname ulak
%global sname ulak
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global redis_make_flags ENABLE_REDIS=1

%if 0%{?rhel} && 0%{?rhel} < 9
%global redis_make_flags %{nil}
%endif

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
Version:	0.2.0
Release:	1PGSTY%{?dist}
Summary:	Transactional outbox extension with background-worker delivery
License:	Apache-2.0
URL:		https://github.com/zeybek/ulak
Source0:	%{sname}-%{version}.tar.gz
Patch0:		ulak-0.2.0.patch
#           https://github.com/zeybek/ulak/archive/refs/tags/v0.2.0.tar.gz
#           Built with HTTP, Kafka, MQTT, Redis, and AMQP dispatchers on EL9; upstream NATS support is left disabled because cnats packages are unavailable in the builder repos

BuildRequires:	gcc
BuildRequires:	libcurl-devel
BuildRequires:	openssl-devel
BuildRequires:	librdkafka-devel
BuildRequires:	mosquitto-devel
%if 0%{?rhel} >= 9 || 0%{?rhel} == 0
BuildRequires:	hiredis-devel
%endif
BuildRequires:	librabbitmq-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
ulak implements the transactional outbox pattern inside PostgreSQL, committing
messages atomically with business transactions and delivering them
asynchronously from background workers. This package enables the HTTP, Kafka,
MQTT, and AMQP dispatchers on all EL builders. Redis Streams support stays
enabled on EL9+ where the packaged hiredis headers include TLS support;
EL8 falls back to the other dispatchers because EPEL's hiredis 0.13 headers do
not ship `hiredis_ssl.h`. Upstream NATS support remains disabled until cnats
development packages are available in the build environment.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} ENABLE_KAFKA=1 ENABLE_MQTT=1 %{?redis_make_flags} ENABLE_AMQP=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} ENABLE_KAFKA=1 ENABLE_MQTT=1 %{?redis_make_flags} ENABLE_AMQP=1 install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%doc README.md
%license LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.2.0-1PGSTY
- Update to 0.2.0

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.0.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 0.0.3
- Rebase the hiredis and libcurl compatibility patch

* Sat Apr 18 2026 Vonng <rh@vonng.com> - 0.0.2-1PIGSTY
- Disable the Redis dispatcher on EL8, where the available hiredis 0.13 headers do not ship hiredis_ssl.h

* Thu Apr 16 2026 Vonng <rh@vonng.com> - 0.0.2-1PIGSTY
- Initial RPM release from the official PGXN 0.0.2 source bundle
- Build the HTTP, Kafka, MQTT, Redis, and AMQP dispatchers on EL9; leave NATS disabled until cnats packages are available
- Fall back to the legacy hiredis keepalive helper on EL9's 1.0.x headers
