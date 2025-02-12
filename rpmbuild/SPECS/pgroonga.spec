%define debug_package %{nil}
%global pname pgroonga
%global sname pgroonga
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

Name:		%{sname}_%{pgmajorversion}
Version:	4.0.0
Release:	1%{?dist}
Summary:	Fast full-text search plugin for PostgreSQL based on Groonga
Group:		Applications/Text
License:	PostgreSQL
URL:		https://pgroonga.github.io/
Source0:	pgroonga-%{version}.tar.gz
#		    https://packages.groonga.org/source/pgroonga/pgroonga-%{version}.tar.gz

BuildRequires:	ccache
BuildRequires:	clang
BuildRequires:	gcc
BuildRequires:	groonga-devel
BuildRequires:	llvm-devel
BuildRequires:	make
BuildRequires:	msgpack-devel
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	xxhash-devel
#BuildRequires:	libpq-devel

Requires:	groonga-libs >= 15.0.0
Requires:	msgpack
Requires:	postgresql%{pgmajorversion}-server
Requires:	xxhash-libs

%description
This package provides a fast full-text search plugin for PostgreSQL based on Groonga

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
Requires:	llvm => 17.0
%endif

%description llvmjit
This package provides JIT support for %{sname}
%endif

%prep
%setup -q -n pgroonga-%{version}

%build
PATH="%{pginstdir}/bin:$PATH" \
  PKG_CONFIG_PATH="${PWD}" \
  make \
    HAVE_MSGPACK=1 \
    HAVE_XXHASH=1 \
    enable_rpath=no \
    %{?_smp_mflags}

%install
PATH="%{pginstdir}/bin:$PATH" \
  make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{sname}_%{pgmajorversion} <<EOF
/var/lib/pgsql/*/data/pgroonga.log {
    weekly
    missingok
    rotate 10
    compress
    delaycompress
    notifempty
    su postgres postgres
}
EOF

%files
%doc README.md COPYING
%config(noreplace) %{_sysconfdir}/logrotate.d/%{sname}_%{pgmajorversion}
%{pginstdir}/bin/pgroonga-generate-primary-maintainer-service.sh
%{pginstdir}/bin/pgroonga-generate-primary-maintainer-timer.sh
%{pginstdir}/bin/pgroonga-primary-maintainer.sh
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql
%{pginstdir}/lib/*.so
%{pginstdir}/include/server/contrib/pgroonga_check/
%{pginstdir}/include/server/contrib/pgroonga_crash_safer/
%{pginstdir}/include/server/contrib/pgroonga_standby_maintainer/
%{pginstdir}/include/server/contrib/pgroonga_wal_applier/
%{pginstdir}/include/server/contrib/pgroonga_wal_resource_manager/
%{pginstdir}/include/server/extension/pgroonga/
%{pginstdir}/include/server/extension/pgroonga_database/
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 4.0.0
* Sat Dec 21 2024 Vonng <rh@vonng.com> - 3.2.5
- Initial RPM release, used by Pigsty <https://pigsty.io>