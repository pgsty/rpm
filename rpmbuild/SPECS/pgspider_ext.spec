%global sname pgspider_ext
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.3.0
Release:        1PGSTY%{?dist}
Summary:        Foreign data wrapper for remote PGSpider servers
License:        PostgreSQL
URL:            https://github.com/pgspider/%{sname}
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pgspider_ext-1.3.0.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:       postgresql%{pgmajorversion}-server

%description
pgspider_ext enables PostgreSQL to access remote PGSpider servers and combine
data from multiple foreign data wrappers through a partitioned-table interface.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?pgmajorversion} >= 18
%patch -P 0 -p1
%endif

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license License
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.3.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Jul 22 2026 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
- Initial RPM release with PostgreSQL 18 compatibility
