%global sname pg_stat_monitor
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Query Performance Monitoring Tool
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.0
Release:	1PIGSTY%{?dist}
License:	PostgreSQL
URL:		https://github.com/percona/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.1.3-2

%description
The pg_stat_monitor is a Query Performance Monitoring tool for PostgreSQL.
It attempts to provide a more holistic picture by providing much-needed query
performance insights in a single view.

pg_stat_monitor provides improved insights that allow database users to
understand query origins, execution, planning statistics and details, query
information, and metadata. This significantly improves observability, enabling
users to debug and tune query performance. pg_stat_monitor is developed on the
basis of pg_stat_statements as its more advanced replacement.

While pg_stat_statements provides ever-increasing metrics, pg_stat_monitor
aggregates the collected data, saving user efforts for doing it themselves.
pg_stat_monitor stores statistics in configurable time-based units – buckets.
This allows focusing on statistics generated for shorter time periods and
makes query timing information such as max/min/mean time more accurate.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_stat_monitor
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0
%endif

%description llvmjit
This packages provides JIT support for pg_stat_monitor
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Nov 08 2025 Vonng <rh@vonng.com> - 2.3.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>