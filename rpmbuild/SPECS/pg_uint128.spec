%global pname uint128
%global sname pg_uint128
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
Version:	1.2.0
Release:	1PGSTY%{?dist}
Summary:	A PostgreSQL extension that adds native support for unsigned integers and 128-bit signed/unsigned integer types.
License:	PostgreSQL
URL:		https://github.com/pg-uint/pg-uint128
Source0:	pg-uint128-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_uint128 is an extension to support similarity queries on PostgreSQL.
The implementation is tightly integrated in the RDBMS in the sense that it
defines operators so instead of the traditional operators (= and <>)
you can use ~~~ and ! (any of these operators represents a similarity function).

%prep
%setup -q -n pg-uint128-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
- https://github.com/pg-uint/pg-uint128/releases/tag/1.2.0
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.1.1-1PIGSTY
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
* Sun Oct 20 2024 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
