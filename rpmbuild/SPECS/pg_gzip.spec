%global pname gzip
%global sname pgsql_gzip
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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.1
Release:	1PGSTY%{?dist}
Summary:	Gzip compress and decompress for PostgreSQL
License:	MIT
URL:		https://github.com/pramsey/pgsql-gzip
Source0:	pgsql-gzip-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	zlib-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Provides:	pg_gzip_%{pgmajorversion} = %{version}-%{release}
Obsoletes:	pg_gzip_%{pgmajorversion} < %{version}-%{release}

%description
Sometimes you just need to compress your bytea object before you return it to the client.
Sometimes you receive a compressed bytea from the client, and you have to uncompress it before you can work with it.
This extension is for that.

%prep
%setup -q -n pgsql-gzip-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.1.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 1.1.1

* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Update to 1.1.0
* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.0.0-4PIGSTY
- Rename RPM package name to pgsql_gzip
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.0.0-2PIGSTY
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
