%global pname pgroonga
%global sname pgroonga
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
Version:	4.0.8
Release:	1PGSTY%{?dist}
Summary:	Fast full-text search plugin for PostgreSQL based on Groonga
Group:		Applications/Text
License:	PostgreSQL
URL:		https://pgroonga.github.io/
Source0:	pgroonga-%{version}.tar.gz

BuildRequires:	ccache
BuildRequires:	gcc
BuildRequires:	groonga-devel >= 15.1.7
BuildRequires:	make
BuildRequires:	meson
BuildRequires:	msgpack-devel
BuildRequires:	ninja-build
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	xxhash-devel
#BuildRequires:	libpq-devel

Requires:	groonga-libs >= 15.1.7
Requires:	msgpack
Requires:	postgresql%{pgmajorversion}-server
Requires:	xxhash-libs

%description
This package provides a fast full-text search plugin for PostgreSQL based on Groonga

%prep
%setup -q -n pgroonga-%{version}

%build
%set_build_flags
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
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 4.0.8-1PGSTY
- Build with the upstream Meson workflow and retain Groonga 15.1 ABI support
* Wed Oct 29 2025 Vonng <rh@vonng.com> - 4.0.4-1PIGSTY
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 4.0.0-1PIGSTY
* Sat Dec 21 2024 Vonng <rh@vonng.com> - 3.2.5-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
