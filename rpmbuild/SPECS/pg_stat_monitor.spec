%global sname pg_stat_monitor
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	PostgreSQL Query Performance Monitoring Tool
Name:		%{sname}_%{pgmajorversion}
Version:	2.4.0
Release:	1PGSTY%{?dist}
License:	PostgreSQL
URL:		https://github.com/percona/%{sname}
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

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

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

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
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/
%endif

%changelog
* Sat Sep 19 2026 Vonng <rh@vonng.com> - 2.4.0-1PGSTY
- Update to 2.4.0

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.3.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Aug 11 2026 Vonng <rh@vonng.com> - 2.3.2-1PIGSTY
- Update to 2.3.2
- https://github.com/percona/pg_stat_monitor/releases/tag/2.3.2
* Mon Dec 01 2025 Vonng <rh@vonng.com> - 2.3.1-1PIGSTY
* Sat Nov 08 2025 Vonng <rh@vonng.com> - 2.3.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
