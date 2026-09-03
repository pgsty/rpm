%global pname sslutils
%global sname sslutils
%global pginstdir /usr/pgsql-%{pgmajorversion}
%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:sslutils 1.4.1 supports PostgreSQL 14 through 18 in Pigsty builds}
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.4.1
Release:	1PGSTY%{?dist}
Summary:	A Postgres extension for managing SSL certificates through SQL.
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/sslutils
Source0:	sslutils-%{version}.tar.gz
Patch0:		sslutils-1.4.1.patch

BuildRequires:	clang gcc llvm make openssl-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
SSLUtils is a Postgres extension that provides SSL certicate generation
functions to Postgres, for use by the Postgres Enterprise Manager server.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install README-sslutils.txt
%{__install} -d -m 755 %{buildroot}%{pginstdir}/share/doc/extension
%{__cp} README.%{sname} %{buildroot}%{pginstdir}/share/doc/extension/README-%{sname}.txt

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%license LICENSE
%attr(644,root,root) %{pginstdir}/share/doc/extension/README-%{sname}.txt
%{pginstdir}/lib/sslutils.so
%{pginstdir}/share/extension/sslutils*.sql
%{pginstdir}/share/extension/uninstall_sslutils.sql
%{pginstdir}/share/extension/sslutils.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 1.4.1-1PGSTY
- Upgrade to upstream sslutils 1.4.1
- Use the repository PostgreSQL license as the packaging license authority
- Retire the obsolete PostgreSQL 18 OpenSSL compatibility patch
- Preserve legacy function OIDs, ACLs, comments, and dependents on upgrade
- Reject sibling-prefix and non-canonical certificate paths
- Require pg_read_server_files for private-key file access

* Wed Jul 22 2026 Vonng <rh@vonng.com> - 1.4-3PIGSTY
- Add PostgreSQL 18 OpenSSL API compatibility

* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.4-2PIGSTY
* Sat Nov 02 2024 Vonng <rh@vonng.com> - 1.4-1PIGSTY
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
