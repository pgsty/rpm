%define __jar_repack %{nil}
%define _build_id_links none
%global debug_package %{nil}

Name:           cloudberry-pxf
Version:        2.1.0
Release:        1PIGSTY%{?dist}
Summary:        Apache Cloudberry PXF for advanced external data access

License:        Apache-2.0
URL:            https://cloudberry.apache.org
Source0:        apache-cloudberry-pxf-2.1.0-incubating-src.tar.gz
Source1:        cloudberry-pxf-2.1.0-rpm-patches.tar.gz
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
* Thu Apr 16 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Initial RPM package for Apache Cloudberry PXF 2.1.0 (incubating)
- Bundle packaging patches into SRPM and ship NOTICE
