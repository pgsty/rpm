%define __jar_repack %{nil}
%define _build_id_links none
%global debug_package %{nil}

Name:           cloudberry-pxf
Version:        2.1.0
Release:        2PIGSTY%{?dist}
Summary:        Apache Cloudberry PXF for advanced external data access

License:        Apache-2.0
URL:            https://cloudberry.apache.org
Source0:        apache-cloudberry-pxf-2.1.0-incubating-src.tar.gz
Source1:        cloudberry-pxf-2.1.0-rpm-patches.tar.gz
Source2:        gradle-wrapper-6.8.2.jar
Source3:        gradle-wrapper-6.8.2.jar.sha256
Source4:        gradle-wrapper-8.5.jar
Source5:        gradle-wrapper-8.5.jar.sha256
Source6:        gradle-6.8.2-bin.zip
Source7:        gradle-8.5-bin.zip
Prefix:         /usr/local/cloudberry-pxf-%{version}
ExclusiveArch:  x86_64 aarch64

AutoReqProv:    no

BuildRequires:  cloudberry = %{version}-%{release}
BuildRequires:  curl gcc gcc-c++ golang libcurl-devel make tar unzip which
%if 0%{?rhel} >= 10
BuildRequires:  java-21-openjdk-devel
%global pxf_java_home /usr/lib/jvm/java-21-openjdk
Suggests:       java-21-openjdk-headless
%else
BuildRequires:  java-11-openjdk-devel
%global pxf_java_home /usr/lib/jvm/java-11-openjdk
Suggests:       java-11-openjdk-headless
%endif
Requires:       bash
Requires:       cloudberry = %{version}-%{release}

%description
Apache Cloudberry PXF (Platform Extension Framework) provides Cloudberry
connectors for external data systems together with the PXF service and CLI.

%prep
%setup -q -n apache-cloudberry-pxf-%{version}
mkdir -p .rpm-patches
tar -xzf %{SOURCE1} -C .rpm-patches
patch -p1 --forward -f < .rpm-patches/cloudberry-pxf-2.1.0-java-utf8.patch
%if 0%{?rhel} >= 10
patch -p1 --forward -f < .rpm-patches/cloudberry-pxf-2.1.0-el10-java21-build-fixes.patch
%endif
%if 0%{?rhel} >= 10
cp -fp %{SOURCE4} server/gradle/wrapper/gradle-wrapper.jar
cp -fp %{SOURCE5} server/gradle/wrapper/gradle-wrapper-8.5.jar.sha256
cp -fp %{SOURCE7} server/gradle/wrapper/gradle-8.5-bin.zip
sed -i "s#^distributionUrl=.*#distributionUrl=file://$(pwd)/server/gradle/wrapper/gradle-8.5-bin.zip#" server/gradle/wrapper/gradle-wrapper.properties
%else
cp -fp %{SOURCE2} server/gradle/wrapper/gradle-wrapper.jar
cp -fp %{SOURCE3} server/gradle/wrapper/gradle-wrapper-6.8.2.jar.sha256
cp -fp %{SOURCE6} server/gradle/wrapper/gradle-6.8.2-bin.zip
sed -i "s#^distributionUrl=.*#distributionUrl=file://$(pwd)/server/gradle/wrapper/gradle-6.8.2-bin.zip#" server/gradle/wrapper/gradle-wrapper.properties
%endif

%build
export GPHOME=/usr/local/cloudberry-%{version}
%if 0%{?rhel} >= 10
export QA_RPATHS=3
%endif
if [ -f "${GPHOME}/cloudberry-env.sh" ]; then
  . "${GPHOME}/cloudberry-env.sh"
elif [ -f "${GPHOME}/greenplum_path.sh" ]; then
  . "${GPHOME}/greenplum_path.sh"
else
  echo "Cloudberry environment script not found under ${GPHOME}" >&2
  exit 1
fi
export PXF_HOME=%{prefix}
export JAVA_HOME=%{pxf_java_home}
export GOPATH=%{_builddir}/go
export GOBIN=${GOPATH}/bin
export GOPROXY=https://goproxy.cn,direct
export PATH=${JAVA_HOME}/bin:${GOBIN}:/usr/local/go/bin:$PATH

make -C external-table stage
make -C fdw stage
make -C cli build
mkdir -p cli/build/stage/bin
cp -fp cli/build/pxf-cli cli/build/stage/bin/pxf-cli
make -C server stage-notest

%install
rm -rf %{buildroot}
%if 0%{?rhel} >= 10
export QA_RPATHS=3
%endif
mkdir -p %{buildroot}%{prefix}
cp -a external-table/build/stage/. %{buildroot}%{prefix}/
cp -a fdw/build/stage/. %{buildroot}%{prefix}/
cp -a cli/build/stage/. %{buildroot}%{prefix}/
cp -a server/build/stage/. %{buildroot}%{prefix}/
install -Dpm 0644 version %{buildroot}%{prefix}/version
install -Dpm 0644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -Dpm 0644 NOTICE %{buildroot}%{_docdir}/%{name}/NOTICE
printf 'apache-cloudberry-pxf-%{version}-source-release\n' > %{buildroot}%{prefix}/commit.sha
mkdir -p %{buildroot}/usr/local
ln -sfn cloudberry-pxf-%{version} %{buildroot}/usr/local/cloudberry-pxf

%post
sed -i "s|directory =.*|directory = '${RPM_INSTALL_PREFIX}/gpextable/'|g" "${RPM_INSTALL_PREFIX}/gpextable/pxf.control"
sed -i "s|module_pathname =.*|module_pathname = '${RPM_INSTALL_PREFIX}/gpextable/pxf'|g" "${RPM_INSTALL_PREFIX}/gpextable/pxf.control"

if [ -f "${RPM_INSTALL_PREFIX}/fdw/pxf_fdw.control" ]; then
  sed -i "s|directory =.*|directory = '${RPM_INSTALL_PREFIX}/fdw/'|g" "${RPM_INSTALL_PREFIX}/fdw/pxf_fdw.control"
  sed -i "s|module_pathname =.*|module_pathname = '${RPM_INSTALL_PREFIX}/fdw/pxf_fdw'|g" "${RPM_INSTALL_PREFIX}/fdw/pxf_fdw.control"
fi

if id "gpadmin" &>/dev/null; then
  chown -R gpadmin:gpadmin ${RPM_INSTALL_PREFIX}
fi

%pre
rm -f "${RPM_INSTALL_PREFIX}/conf/pxf-private.classpath"
rm -rf "${RPM_INSTALL_PREFIX}/pxf-service"

%posttrans
install -d -m 700 "${RPM_INSTALL_PREFIX}/run"

%preun
if [ $1 -eq 0 ] ; then
  rm -f /usr/local/cloudberry-pxf
fi

%files
%exclude %{prefix}/conf/pxf-application.properties
%exclude %{prefix}/conf/pxf-env.sh
%exclude %{prefix}/conf/pxf-log4j2.xml
%exclude %{prefix}/conf/pxf-profiles.xml
%{prefix}
/usr/local/cloudberry-pxf
%license /usr/share/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/NOTICE

%config(noreplace) %{prefix}/conf/pxf-application.properties
%config(noreplace) %{prefix}/conf/pxf-env.sh
%config(noreplace) %{prefix}/conf/pxf-log4j2.xml
%config(noreplace) %{prefix}/conf/pxf-profiles.xml

%changelog
* Sun Apr 19 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-2PIGSTY
- Rebuild for EL10 together with the Cloudberry initdb fix release
- Use a mirrored local Gradle 8.5 distribution on EL10 builders

* Sat Apr 18 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Route Go module downloads through goproxy.cn for builder connectivity
- Pre-seed Gradle wrapper artifacts to avoid GitHub raw fetches during build
- Pre-seed Gradle 6.8.2 distribution for EL8/EL9 wrapper timeouts

* Thu Apr 16 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Initial RPM package for Apache Cloudberry PXF 2.1.0 (incubating)
- Bundle packaging patches into SRPM and ship NOTICE
