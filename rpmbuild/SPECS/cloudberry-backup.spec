%global debug_package %{nil}
%global _build_id_links none

Name:           cloudberry-backup
Version:        2.1.0
Release:        3PIGSTY%{?dist}
Summary:        Backup and restore utilities for Apache Cloudberry

License:        Apache-2.0
URL:            https://cloudberry.apache.org
Source0:        apache-cloudberry-backup-2.1.0-incubating-src.tar.gz
ExclusiveArch:  x86_64 aarch64
%global cb_prefix /usr/cloudberry

BuildRequires:  gcc golang >= 1.21 make sqlite-devel
Requires:       bash
Requires:       cloudberry = %{version}-%{release}

%description
Cloudberry Backup packages the gpbackup, gprestore, gpbackup_helper, and
gpbackup_s3_plugin utilities for Apache Cloudberry.

%prep
%setup -q -n apache-cloudberry-backup-%{version}

%build
export GOPATH=%{_builddir}/go
export GOPROXY=https://goproxy.cn,direct
export PATH=${GOPATH}/bin:/usr/local/go/bin:$PATH
make depend
make build

%install
rm -rf %{buildroot}
install -Dpm 0755 %{_builddir}/go/bin/gpbackup %{buildroot}%{cb_prefix}/bin/gpbackup
install -Dpm 0755 %{_builddir}/go/bin/gprestore %{buildroot}%{cb_prefix}/bin/gprestore
install -Dpm 0755 %{_builddir}/go/bin/gpbackup_helper %{buildroot}%{cb_prefix}/bin/gpbackup_helper
install -Dpm 0755 %{_builddir}/go/bin/gpbackup_s3_plugin %{buildroot}%{cb_prefix}/bin/gpbackup_s3_plugin
install -Dpm 0644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -Dpm 0644 NOTICE %{buildroot}%{_docdir}/%{name}/NOTICE

%files
%{cb_prefix}/bin/gpbackup
%{cb_prefix}/bin/gprestore
%{cb_prefix}/bin/gpbackup_helper
%{cb_prefix}/bin/gpbackup_s3_plugin
%license /usr/share/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/NOTICE

%changelog
* Tue Jul 07 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-3PIGSTY
- Install backup tools into /usr/cloudberry/bin to match the DEB package

* Sun Apr 19 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-2PIGSTY
- Rebuild for EL10 together with the Cloudberry initdb fix release

* Sat Apr 18 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Route Go module downloads through goproxy.cn for builder connectivity

* Thu Apr 16 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Initial RPM package for Apache Cloudberry Backup 2.1.0 (incubating)
