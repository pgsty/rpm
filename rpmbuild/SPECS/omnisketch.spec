%global pname omnisketch
%global sname omnisketch
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
Version:	1.0.2
Release:	1PGSTY%{?dist}
Summary:	OmniSketch, a data structure for on-line aggregation of data into approximate sketch, and answering queries
License:	PostgreSQL
URL:		https://github.com/tvondra/omnisketch
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 xxhash-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements OmniSketch, a data structure for on-line aggregation of data into approximate sketch,
and answering queries. The algorithm is also very friendly to parallel programs.
The OmniSketch data structure was introduced by this paper:
OmniSketch: Efficient Multi-Dimensional High-Velocity Stream Analytics with Arbitrary Predicates;
Wieger R. Punter, Odysseas Papapetrou, Minos Garofalakis; Proc. {VLDB} Endow. Volume 17, No. 3, p 319-331, 2023

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jan 09 2025 Vonng <rh@vonng.com> - 1.0.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
