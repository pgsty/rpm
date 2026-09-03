%global pname zhparser
%global sname zhparser
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
Version:	2.3
Release:	1PGSTY%{?dist}
Summary:	Open-source full-text search of Chinese language
License:	PostgreSQL
URL:		https://github.com/amutu/zhparser/
Source0:	zhparser-%{version}.tar.gz
#           https://github.com/amutu/zhparser/archive/refs/tags/V2.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server scws

%description
zhparser is a PostgreSQL extension for full-text search of Chinese language (Mandarin Chinese).
It implements a Chinese language parser base on the Simple Chinese Word Segmentation(SCWS).

%prep
%setup -q -n %{sname}-%{version}

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
%{pginstdir}/share/tsearch_data/dict.utf8.xdb
%{pginstdir}/share/tsearch_data/rules.utf8.ini
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Feb 11 2025 Vonng <rh@vonng.com> - 2.3
* Wed Sep 13 2023 Vonng <rh@vonng.com> - 2.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
