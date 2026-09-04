%global pname datasketches
%global sname datasketches
%global core_version 5.2.0
%global buildsrc apache-datasketches-postgresql-%{version}-src
%global corebuildsrc apache-datasketches-cpp-%{core_version}-src
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:datasketches supports PostgreSQL 14 through 18 in Pigsty}
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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.7.0
Release:	2PGSTY%{?dist}
Summary:	Apache DataSketches extension for approximate analytics in PostgreSQL
License:	Apache-2.0
URL:		https://github.com/apache/datasketches-postgresql
Source0:	apache-datasketches-postgresql-%{version}-src.tar.gz
#		https://archive.apache.org/dist/datasketches/postgresql/1.7.0/apache-datasketches-postgresql-1.7.0-src.tar.gz
Source1:	apache-datasketches-cpp-%{core_version}-src.tar.gz
#		https://downloads.apache.org/datasketches/cpp/5.2.0/apache-datasketches-cpp-5.2.0-src.zip
Patch0:		datasketches-1.7.0-core-5.2.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc-c++
BuildRequires:	boost-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Apache DataSketches brings approximate analytics data types and aggregates to
PostgreSQL. The extension includes CPC, HLL, Theta, Array-of-Doubles, KLL,
REQ, quantiles, and frequent-strings sketches for fast approximate distinct
counting, quantiles, histograms, and heavy-hitter analysis.

%prep
%{__rm} -rf %{_builddir}/%{corebuildsrc}
%setup -q -n %{buildsrc}
cd %{_builddir}
tar -xf %{SOURCE1}
patch -d %{buildsrc} -p1 --fuzz=0 < %{PATCH0}

%build
cd %{_builddir}/%{buildsrc}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} \
  CORE=%{_builddir}/%{corebuildsrc} \
  BOOST=/usr/include

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{buildsrc}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} \
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
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.7.0-2PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Rebuild the current PostgreSQL extension with DataSketches C++ core 5.2.0
- Normalize the official Apache zip release into the shared deterministic tarball
- Fix PGXS C++ LLVM builds by including cstdint explicitly
- Restore automatic debuginfo and debugsource generation with %setup

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.7.0-1PIGSTY
- Initial RPM release based on Apache DataSketches PostgreSQL 1.7.0
- Build against Apache DataSketches C++ core 5.0.0 and system boost-devel
