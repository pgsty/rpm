%global pname pgroonga
%global sname pgroonga
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?rhel} == 9
# Require the repaired ABI provider while allowing newer upstream releases.
%global groonga_min_version 16.1.3-1.el9.PGSTY.1
%else
%global groonga_min_version 15.1.7
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

Name:		%{sname}_%{pgmajorversion}
Version:	4.1.0
%if 0%{?rhel} == 9
Release:	2PGSTY%{?dist}
%else
Release:	1PGSTY%{?dist}
%endif
Summary:	Fast full-text search plugin for PostgreSQL based on Groonga
Group:		Applications/Text
License:	PostgreSQL
URL:		https://pgroonga.github.io/
Source0:	pgroonga-%{version}.tar.gz

BuildRequires:	ccache
BuildRequires:	gcc
BuildRequires:	groonga-devel >= %{groonga_min_version}
BuildRequires:	make
BuildRequires:	meson
BuildRequires:	msgpack-devel
BuildRequires:	ninja-build
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	xxhash-devel
#BuildRequires:	libpq-devel

Requires:	groonga-libs >= %{groonga_min_version}
Requires:	msgpack
Requires:	postgresql%{pgmajorversion}-server
Requires:	xxhash-libs

%description
This package provides a fast full-text search plugin for PostgreSQL based on Groonga

%prep
%setup -q -n pgroonga-%{version}

%build
%set_build_flags
# Upstream Meson builds shared modules only; it has no LLVM bitcode target.
meson setup build \
  -Dinstall_to_postgresql=true \
  -Dmessage_pack=enabled \
  -Dtest=false \
  -Dxxhash=enabled \
  -Dpg_config=%{pginstdir}/bin/pg_config
meson compile -C build

%install
DESTDIR=$RPM_BUILD_ROOT meson install -C build

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
%{pginstdir}/share/pgroonga/
%{pginstdir}/lib/*.so

%changelog
* Thu Oct 15 2026 Vonng <rh@vonng.com> - 4.1.0-2PGSTY
- Rebuild EL9 packages against the repaired Groonga system simdjson ABI.
- Require the fixed EL9 Groonga release and allow later upstream releases.

* Sat Oct 10 2026 Vonng <rh@vonng.com> - 4.1.0-1PGSTY
- Update pgroonga and pgroonga_database to upstream 4.1.0.
- Retain the Meson build and the supported Groonga 15.1 ABI baseline.

* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 4.0.9-1PGSTY
- Update to 4.0.9.

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 4.0.8-1PGSTY
- Build with the upstream Meson workflow and retain Groonga 15.1 ABI support
* Wed Oct 29 2025 Vonng <rh@vonng.com> - 4.0.4-1PIGSTY
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 4.0.0-1PIGSTY
* Sat Dec 21 2024 Vonng <rh@vonng.com> - 3.2.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
