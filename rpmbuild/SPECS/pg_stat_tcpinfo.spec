%global pname pg_stat_tcpinfo
%global sname pg_stat_tcpinfo
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_stat_tcpinfo is packaged for PostgreSQL 14, 15, 16, 17, 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.1
Release:        1PGSTY%{?dist}
Summary:        Detailed Linux TCP socket statistics for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/jakubwartakEDB/pg_stat_tcpinfo
Source0:        %{sname}-%{version}.tar.gz
# Official archive: https://api.github.com/repos/jakubwartakEDB/pg_stat_tcpinfo/tarball/v1.1
# SHA256: 4dc16ce383bd511abf95224593babdcf77ae3a55b18aee4b34568dbb5d8db868

BuildRequires:  gcc make
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server

%description
Expose TCP connections owned by the PostgreSQL server OS user, including
round-trip time, retransmissions, congestion control and queue statistics.
Requires Linux 4.18 or newer with procfs and NETLINK_INET_DIAG.
Access is restricted to PostgreSQL monitoring roles; no preload is needed.

%prep
%setup -q -n jakubwartakEDB-pg_stat_tcpinfo-fc5b47b

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/pg_stat_tcpinfo.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%{pginstdir}/lib/bitcode/pg_stat_tcpinfo/
%{pginstdir}/lib/bitcode/pg_stat_tcpinfo.index.bc
%endif
%exclude /usr/lib/.build-id

%changelog
* Wed Oct 28 2026 Ruohang Feng <rh@vonng.com> - 1.1-1PGSTY
- Initial RPM release with native debug information and PGXS bitcode.
