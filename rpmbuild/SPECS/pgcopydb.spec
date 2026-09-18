%global sname pgcopydb
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgcopydb supports PostgreSQL 14 through 18 in Pigsty}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.18
Release:        1PGSTY%{?dist}
Summary:        Copy an entire PostgreSQL database from source to target
License:        PostgreSQL AND MIT
URL:            https://github.com/dimitri/pgcopydb
Source0:        %{sname}-%{version}.tar.gz

BuildRequires:  gcc make pgdg-srpm-macros >= 1.0.27
BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  gc-devel ncurses-devel numactl-devel
BuildRequires:  libedit-devel readline-devel
BuildRequires:  libselinux-devel libxslt-devel
BuildRequires:  krb5-devel lz4-devel openssl-devel pam-devel
BuildRequires:  libzstd-devel zlib-devel
Requires:       postgresql%{pgmajorversion}

%description
pgcopydb copies an entire PostgreSQL database from source to target. It
combines pg_dump and pg_restore with advanced concurrency and resumable
catalog state to make migrations faster and easier to operate.

%prep
%autosetup -p1 -n %{sname}-%{version}
%if 0%{?rhel} == 8
%ifarch aarch64
# Pass PIE to the compiler driver so EL8 selects the position-independent CRT.
sed -i 's/-fpie -Wl,-pie/-fpie -pie/' src/bin/pgcopydb/Makefile
%endif
%endif

%build
%{__make} -C src/bin/pgcopydb \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    GIT_VERSION=%{version} git-version.h
%{__make} -C src/bin/pgcopydb %{?_smp_mflags} \
    PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__make} -C src/bin/pgcopydb install \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    DESTDIR=%{buildroot} BINDIR=%{pginstdir}/bin

%check
src/bin/pgcopydb/pgcopydb --version | grep -F 'pgcopydb version %{version}'

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/bin/%{sname}

%changelog
* Wed Sep 09 2026 Ruohang Feng <rh@vonng.com> - 0.18-1PGSTY
- Select the PIE startup objects when linking on EL8 aarch64

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.18-1PGSTY
- Initial Pigsty RPM package for pgcopydb 0.18
- Package one binary per supported PostgreSQL major to keep client tools aligned
