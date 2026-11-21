%global pname pg_stl
%global sname pg_stl
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

%if 0%{?pgmajorversion} < 16
%{error:pg_stl only supports PostgreSQL 16+}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PGSTY%{?dist}
Summary:	Time series analysis functions for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/nadyaloseva/pg_ts_analysis
Source0:	%{sname}-%{version}.tar.gz
Patch0:        pg_stl-1.0.0-pg19-tuple-header.patch
#           normalized from https://api.pgxn.org/dist/pg_stl/1.0.0/pg_stl-1.0.0.zip
#           Supported: PostgreSQL 16, 17, 18

BuildRequires:	gcc
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%if %llvm
BuildRequires: llvm-devel >= 19.0
BuildRequires: clang-devel >= 19.0
%endif

%description
pg_stl provides time series analysis functions for PostgreSQL, including ACF,
PACF, STL decomposition, and Holt-Winters forecasting.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} %{with_llvm_arg}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*
%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 1.0.0-1PGSTY
- Add PostgreSQL 19 header and type compatibility.

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.0
