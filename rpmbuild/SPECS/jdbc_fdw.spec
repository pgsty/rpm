%global sname jdbc_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:jdbc_fdw supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

# Keep the embedded JVM aligned with the JDK selected by the PGDG PL/Java
# package on each Enterprise Linux release.  In particular, unversioned
# java-devel resolves to Java 8 on EL8, which PL/Java 1.6.x does not support.
%if 0%{?rhel} == 8
%global java_home /etc/alternatives/java_sdk_11_openjdk
%global java_runtime_home /usr/lib/jvm/jre-11-openjdk
%global java_devel java-11-openjdk-devel
%global java_runtime java-11-openjdk-headless
%else
%if 0%{?rhel} == 9
%global java_home /usr/lib/jvm/java-openjdk
%global java_runtime_home /usr/lib/jvm/jre-17-openjdk
%global java_devel java-17-openjdk-devel
%global java_runtime java-17-openjdk-headless
%else
%global java_home /usr/lib/jvm/java-openjdk
%global java_runtime_home /usr/lib/jvm/jre-21-openjdk
%global java_devel java-21-openjdk-devel
%global java_runtime java-21-openjdk-headless
%endif
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.5.0
Release:        1PIGSTY%{?dist}
Summary:        JDBC Foreign Data Wrapper for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/pgspider/%{sname}
Source0:        %{sname}-%{version}.tar.gz
Patch0:         %{sname}-%{version}-portable-jvm.patch
Patch1:         %{sname}-%{version}-pg18.patch

BuildRequires:  gcc make pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  %{java_devel}
Requires:       postgresql%{pgmajorversion}-server
Requires:       %{java_runtime}

%description
jdbc_fdw is a PostgreSQL foreign data wrapper for connecting to any data
source that provides a Java Database Connectivity (JDBC) driver.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for jdbc_fdw
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for jdbc_fdw.
%endif

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
export JAVA_HOME=%{java_home}
export PATH=%{java_home}/bin:%{pginstdir}/bin:$PATH
%{__make} %{?_smp_mflags} USE_PGXS=1 \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    LIBDIR=%{java_home}/lib/server \
    rpathdir='$$ORIGIN' \
    JAVAC=%{java_home}/bin/javac JAVACFLAGS="--release 8"

%install
%{__rm} -rf %{buildroot}
export JAVA_HOME=%{java_home}
export PATH=%{java_home}/bin:%{pginstdir}/bin:$PATH
%{__make} install USE_PGXS=1 \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    LIBDIR=%{java_home}/lib/server \
    rpathdir='$$ORIGIN' \
    JAVAC=%{java_home}/bin/javac JAVACFLAGS="--release 8" \
    DESTDIR=%{buildroot}

# jdbc_fdw.so uses an $ORIGIN RUNPATH.  Keep a package-owned link beside the
# extension so the dynamic loader reaches the matching versioned JRE without
# embedding an architecture-specific absolute path.
%{__ln_s} %{java_runtime_home}/lib/server/libjvm.so \
    %{buildroot}%{pginstdir}/lib/libjvm.so

%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md \
    %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE.md
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/libjvm.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/*.class

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%{pginstdir}/lib/bitcode/%{sname}/
%endif

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 0.5.0-1PIGSTY
- Initial PGSTY RPM release for PostgreSQL 14 through 18
- Align the embedded JVM with PL/Java: JDK 11 on EL8, 17 on EL9, and 21 on EL10
- Add portable x86_64/aarch64 JVM linking and PostgreSQL 18 compatibility
