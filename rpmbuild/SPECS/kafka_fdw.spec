%global pname kafka_fdw
%global sname kafka_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_commit 8615082d986ba11ed70191bb4ca53c8cb7e4def3

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
Version:	0.0.3
Release:	2.git20251030.8615082PGSTY%{?dist}
Summary:	kafka foreign database wrapper for postresql
License:	PostgreSQL
URL:		https://github.com/adjust/kafka_fdw
Source0:	%{sname}-0.0.3+git20251030.8615082.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 librdkafka-devel >= 1.6.0
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
At this point the project is not yet production ready. Use with care. Pull requests welcome
A simple foreign data wrapper for Kafka which allows it to be treated as a table.
Currently kafka_fdw allows message parsing in csv and json format. More might come in a future release.

%prep
%setup -q -n %{sname}-%{snapshot_commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.0.3-2.git20251030.8615082PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Package upstream master snapshot 8615082d986b
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.0.3-2PIGSTY
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.0.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
