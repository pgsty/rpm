%global pname datasketches
%global sname datasketches
%global core_version 5.0.0
%global buildsrc apache-datasketches-postgresql-%{version}-src
%global corebuildsrc apache-datasketches-cpp-%{core_version}-src
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
Version:	1.7.0
Release:	1PIGSTY%{?dist}
Summary:	Apache DataSketches extension for approximate analytics in PostgreSQL
License:	Apache-2.0
URL:		https://github.com/apache/datasketches-postgresql
Source0:	apache-datasketches-postgresql-%{version}-src.tar.gz
#		https://archive.apache.org/dist/datasketches/postgresql/1.7.0/apache-datasketches-postgresql-1.7.0-src.tar.gz
Source1:	apache-datasketches-cpp-%{core_version}-src.tar.gz
#		https://archive.apache.org/dist/datasketches/cpp/5.0.0/apache-datasketches-cpp-5.0.0-src.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++
BuildRequires:	boost-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Apache DataSketches brings approximate analytics data types and aggregates to
PostgreSQL. The extension includes CPC, HLL, Theta, Array-of-Doubles, KLL,
REQ, quantiles, and frequent-strings sketches for fast approximate distinct
counting, quantiles, histograms, and heavy-hitter analysis.

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
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%{__rm} -rf %{_builddir}/%{buildsrc} %{_builddir}/%{corebuildsrc}
cd %{_builddir}
tar -xf %{SOURCE0}
tar -xf %{SOURCE1}

%build
cd %{_builddir}/%{buildsrc}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} \
  CORE=%{_builddir}/%{corebuildsrc} \
  BOOST=/usr/include

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{buildsrc}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} \
  CORE=%{_builddir}/%{corebuildsrc} \
  BOOST=/usr/include
install -m 644 README.md NOTICE %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/
install -m 644 %{_builddir}/%{corebuildsrc}/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE.datasketches-cpp
install -m 644 %{_builddir}/%{corebuildsrc}/NOTICE %{buildroot}%{_docdir}/%{name}/NOTICE.datasketches-cpp

%files
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/LICENSE.datasketches-cpp
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/NOTICE
%doc %{_docdir}/%{name}/NOTICE.datasketches-cpp
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.7.0-1PIGSTY
- Initial RPM release based on Apache DataSketches PostgreSQL 1.7.0
- Build against Apache DataSketches C++ core 5.0.0 and system boost-devel
