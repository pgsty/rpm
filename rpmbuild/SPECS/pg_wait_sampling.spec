%global sname pg_wait_sampling
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.11
Release:	1PGSTY%{?dist}
Summary:	Sampling based statistics of wait events
License:	PostgreSQL
URL:		https://github.com/postgrespro/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL provides information about the current wait event of a particular
process. pg_wait_sampling collects repeated samples to provide descriptive
statistics about server wait-event behavior.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 0644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.1.11-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jul 23 2026 Vonng <rh@vonng.com> - 1.1.11-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
- https://github.com/postgrespro/pg_wait_sampling/releases/tag/v1.1.11
