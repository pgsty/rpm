%global _build_id_links none

Name:           cloudberry-backup
Version:        2.2.0
Release:        1.git20260813.6d61e7ePGSTY%{?dist}
Summary:        Backup and restore utilities for Apache Cloudberry

License:        Apache-2.0
URL:            https://cloudberry.apache.org
Source0:        apache-cloudberry-backup-2.2.0-src.tar.gz
# Deterministic snapshot of apache/cloudberry-backup main commit
# 6d61e7e744243f256c971a90e0b33841cae36aea (VERSION=2.2.0).
ExclusiveArch:  x86_64 aarch64
%global cb_prefix /usr/cloudberry

BuildRequires:  gcc golang >= 1.22 make sqlite-devel
Requires:       bash openssh-clients rsync
Requires:       cloudberry >= 2.1.0

%description
Cloudberry Backup packages the gpbackup, gprestore, gpbackup_helper,
gpbackup_s3_plugin, gpbackman, and gpbackup_exporter utilities for Apache
Cloudberry.

%prep
%setup -q -n apache-cloudberry-backup-%{version}
%if 0%{?rhel} == 8
# EL8's binutils/debugedit cannot decode Go's compressed DWARF sections.
sed -i "s/--ldflags '/--ldflags '-compressdwarf=false /g" Makefile
sed -i 's/-ldflags "/-ldflags "-compressdwarf=false /g' Makefile
%endif

%build
export GOPATH=%{_builddir}/go
export GOPROXY=${GOPROXY:-https://goproxy.cn,direct}
export GOTOOLCHAIN=go1.25.0
# EL debugedit cannot yet read Go's DWARF 5 directory strings. Keep full DWARF 4.
export GOEXPERIMENT=nodwarf5
export SOURCE_DATE_EPOCH=1786614056
export PATH=${GOPATH}/bin:/usr/local/go/bin:$PATH
make depend
make build BUILD_DATE=$(date -u -d @${SOURCE_DATE_EPOCH} '+%%Y%%m%%d-%%H:%%M:%%S')

%install
rm -rf %{buildroot}
install -Dpm 0755 %{_builddir}/go/bin/gpbackup %{buildroot}%{cb_prefix}/bin/gpbackup
install -Dpm 0755 %{_builddir}/go/bin/gprestore %{buildroot}%{cb_prefix}/bin/gprestore
install -Dpm 0755 %{_builddir}/go/bin/gpbackup_helper %{buildroot}%{cb_prefix}/bin/gpbackup_helper
install -Dpm 0755 %{_builddir}/go/bin/gpbackup_s3_plugin %{buildroot}%{cb_prefix}/bin/gpbackup_s3_plugin
install -Dpm 0755 %{_builddir}/go/bin/gpbackman %{buildroot}%{cb_prefix}/bin/gpbackman
install -Dpm 0755 %{_builddir}/go/bin/gpbackup_exporter %{buildroot}%{cb_prefix}/bin/gpbackup_exporter
install -Dpm 0644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -Dpm 0644 NOTICE %{buildroot}%{_docdir}/%{name}/NOTICE

%files
%{cb_prefix}/bin/gpbackup
%{cb_prefix}/bin/gprestore
%{cb_prefix}/bin/gpbackup_helper
%{cb_prefix}/bin/gpbackup_s3_plugin
%{cb_prefix}/bin/gpbackman
%{cb_prefix}/bin/gpbackup_exporter
%license /usr/share/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/NOTICE

%changelog
* Tue Sep 08 2026 Ruohang Feng <rh@vonng.com> - 2.2.0-1.git20260813.6d61e7ePGSTY
- Use a reachable Go module proxy while respecting builder overrides
- Generate DWARF 4 with Go 1.25.0 for EL debugsource compatibility
- Leave Go DWARF sections uncompressed for EL8 binutils and debugedit

* Mon Aug 31 2026 Ruohang Feng <rh@vonng.com> - 2.2.0-1.git20260813.6d61e7ePGSTY
- Update to Apache Cloudberry Backup 2.2.0 main snapshot
- Package gpbackman and gpbackup_exporter
- Use the upstream-required Go 1.25 toolchain

* Tue Jul 07 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-3PIGSTY
- Install backup tools into /usr/cloudberry/bin to match the DEB package

* Sun Apr 19 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-2PIGSTY
- Rebuild for EL10 together with the Cloudberry initdb fix release

* Sat Apr 18 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Route Go module downloads through goproxy.cn for builder connectivity

* Thu Apr 16 2026 Ruohang Feng <rh@vonng.com> - 2.1.0-1PIGSTY
- Initial RPM package for Apache Cloudberry Backup 2.1.0 (incubating)
