%{!?pgmajorversion:%global pgmajorversion 19}
%global sname hdfs_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 19
%{error:This gap-build recipe targets PostgreSQL 19}
%endif
%if 0%{?rhel} == 9
%global java_major 17
%else
%if 0%{?rhel} == 10
%global java_major 21
%else
%{error:This recipe targets Enterprise Linux 9 and 10}
%endif
%endif
%global jdk /usr/lib/jvm/java-%{java_major}-openjdk

%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg LLVM_BINPATH=%{_bindir}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.3.3
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL foreign data wrapper for Hive-compatible servers
License:        PostgreSQL
URL:            https://github.com/EnterpriseDB/hdfs_fdw
Source0:        https://github.com/EnterpriseDB/hdfs_fdw/archive/refs/tags/v%{version}.tar.gz#/%{sname}-%{version}.tar.gz
Patch0:         hdfs_fdw-2.3.3-pg19-version-check.patch
ExclusiveArch:  x86_64 aarch64

BuildRequires:  gcc-c++ make libxml2-devel
BuildRequires:  postgresql%{pgmajorversion}-devel >= 19.0
BuildRequires:  java-%{java_major}-openjdk-devel
%if %llvm
BuildRequires:  clang-devel >= 19.0
BuildRequires:  llvm-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server%{?_isa} >= 19.0
Requires:       java-%{java_major}-openjdk-headless%{?_isa}

%description
Read Hive-compatible remote tables through PostgreSQL foreign tables. The
native JNI library and Java bridge are included. Supply a compatible Hive
JDBC driver on the PostgreSQL server and configure the JVM and class paths.

%prep
%autosetup -n %{sname}-%{version} -p1

%build
%set_build_flags
export PATH=%{pginstdir}/bin:$PATH
export USE_PGXS=1 JDK_INCLUDE=%{jdk}/include
%make_build -C libhive
# PGXS quotes rpathdir in the link command. Make turns $$ into one literal $.
%make_build %{with_llvm_arg} 'rpathdir=$$ORIGIN'
pushd libhive/jdbc
%{jdk}/bin/javac --release 8 MsgBuf.java JDBCType.java HiveJdbcClient.java
%{jdk}/bin/jar cf HiveJdbcClient-1.0.jar MsgBuf.class JDBCType.class HiveJdbcClient.class
popd

%install
export PATH=%{pginstdir}/bin:$PATH
export USE_PGXS=1 JDK_INCLUDE=%{jdk}/include
%make_install %{with_llvm_arg} 'rpathdir=$$ORIGIN'
install -m 0755 libhive/libhive.so %{buildroot}%{pginstdir}/lib/
install -m 0644 libhive/jdbc/HiveJdbcClient-1.0.jar %{buildroot}%{pginstdir}/lib/

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/libhive.so
%{pginstdir}/lib/HiveJdbcClient-1.0.jar
%if %llvm
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%{pginstdir}/lib/bitcode/%{sname}/
%endif
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%changelog
* Tue Nov 24 2026 PGSTY Packaging - 2.3.3-1PGSTY
- Trial PG19 gap build using the upstream sources and the version-gate patch.
