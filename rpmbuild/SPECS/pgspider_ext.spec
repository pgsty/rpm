%global sname pgspider_ext
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:           %{sname}_%{pgmajorversion}
Version:        1.3.0
Release:        1PIGSTY%{?dist}
Summary:        Foreign data wrapper for remote PGSpider servers
License:        PostgreSQL
URL:            https://github.com/pgspider/%{sname}
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pgspider_ext-1.3.0-pg18.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
Requires:       postgresql%{pgmajorversion}-server

%description
pgspider_ext enables PostgreSQL to access remote PGSpider servers and combine
data from multiple foreign data wrappers through a partitioned-table interface.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?pgmajorversion} >= 18
%patch -P 0 -p1
%endif

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license License
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*
%endif

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 1.3.0-1PIGSTY
- Initial RPM release with PostgreSQL 18 compatibility
