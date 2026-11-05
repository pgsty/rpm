%global sname postgres-decoderbufs
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:decoderbufs supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        3.7.0
Release:        1PGSTY%{?dist}
Summary:        Protocol Buffers logical decoding output plugin
License:        MIT
URL:            https://github.com/debezium/postgres-decoderbufs
Source0:        decoderbufs-3.7.0.tar.gz
# https://github.com/debezium/postgres-decoderbufs/tree/v3.7.0.Final

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make protobuf-c-devel pkgconfig
Requires:       postgresql%{pgmajorversion}-server

%{!?llvm:%global llvm 1}
%if %llvm
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

%description
Decoderbufs serializes PostgreSQL logical changes as Protocol Buffers for Debezium.

%prep
%setup -q -n postgres-decoderbufs-3.7.0.Final

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}  %{with_llvm_arg}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make}  %{with_llvm_arg} install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 3.7.0-1PGSTY
- Add the upstream 3.7.0 package for PostgreSQL 14 through 18
