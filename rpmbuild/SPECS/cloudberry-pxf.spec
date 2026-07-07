%define __jar_repack %{nil}
%define _build_id_links none
%global debug_package %{nil}

Name:           cloudberry-pxf
Version:        2.1.0
Release:        3PIGSTY%{?dist}
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
%global cb_prefix /usr/cloudberry
%global pxf_prefix /usr/cloudberry-pxf
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
export GPHOME=%{cb_prefix}
export QA_RPATHS=3
if [ ! -x "${GPHOME}/bin/postgres" ]; then
  echo "cloudberry must be installed under ${GPHOME} before building cloudberry-pxf" >&2
  exit 1
fi
export PXF_HOME=%{pxf_prefix}
export JAVA_HOME=%{pxf_java_home}
export PG_CONFIG=${GPHOME}/bin/pg_config
export GOPATH=%{_builddir}/go
export GOBIN=${GOPATH}/bin
export GOPROXY=https://goproxy.cn,direct
export PATH=${GPHOME}/bin:${JAVA_HOME}/bin:${GOBIN}:/usr/local/go/bin:$PATH

make -C external-table stage
make -C fdw stage
make -C cli build
mkdir -p cli/build/stage/bin
cp -fp cli/build/pxf-cli cli/build/stage/bin/pxf-cli
make -C server stage-notest

%install
rm -rf %{buildroot}
export QA_RPATHS=3
mkdir -p %{buildroot}%{pxf_prefix}
cp -a external-table/build/stage/. %{buildroot}%{pxf_prefix}/
cp -a fdw/build/stage/. %{buildroot}%{pxf_prefix}/
cp -a cli/build/stage/. %{buildroot}%{pxf_prefix}/
cp -a server/build/stage/. %{buildroot}%{pxf_prefix}/
install -Dpm 0644 version %{buildroot}%{pxf_prefix}/version
install -Dpm 0644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -Dpm 0644 NOTICE %{buildroot}%{_docdir}/%{name}/NOTICE
printf 'apache-cloudberry-pxf-%{version}-source-release\n' > %{buildroot}%{pxf_prefix}/commit.sha

%post
sed -i "s|directory =.*|directory = '%{pxf_prefix}/gpextable/'|g" "%{pxf_prefix}/gpextable/pxf.control"
sed -i "s|module_pathname =.*|module_pathname = '%{pxf_prefix}/gpextable/pxf'|g" "%{pxf_prefix}/gpextable/pxf.control"

if [ -f "%{pxf_prefix}/fdw/pxf_fdw.control" ]; then
  sed -i "s|directory =.*|directory = '%{pxf_prefix}/fdw/'|g" "%{pxf_prefix}/fdw/pxf_fdw.control"
  sed -i "s|module_pathname =.*|module_pathname = '%{pxf_prefix}/fdw/pxf_fdw'|g" "%{pxf_prefix}/fdw/pxf_fdw.control"
fi

if id "gpadmin" &>/dev/null; then
  chown -R gpadmin:gpadmin %{pxf_prefix}
fi

%pre
rm -f "%{pxf_prefix}/conf/pxf-private.classpath"
rm -rf "%{pxf_prefix}/pxf-service"

%posttrans
install -d -m 700 "%{pxf_prefix}/run"
if id "gpadmin" &>/dev/null; then
  chown gpadmin:gpadmin "%{pxf_prefix}/run"
fi

%files
%exclude %{pxf_prefix}/conf/pxf-application.properties
%exclude %{pxf_prefix}/conf/pxf-env.sh
%exclude %{pxf_prefix}/conf/pxf-log4j2.xml
%exclude %{pxf_prefix}/conf/pxf-profiles.xml
%{pxf_prefix}
%license /usr/share/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/NOTICE

%config(noreplace) %{pxf_prefix}/conf/pxf-application.properties
%config(noreplace) %{pxf_prefix}/conf/pxf-env.sh
%config(noreplace) %{pxf_prefix}/conf/pxf-log4j2.xml
%config(noreplace) %{pxf_prefix}/conf/pxf-profiles.xml

%changelog
* Tue Jul 07 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-3PIGSTY
- Move PXF to /usr/cloudberry-pxf and build against /usr/cloudberry
- Replace relocatable scriptlets with fixed private-prefix paths

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
