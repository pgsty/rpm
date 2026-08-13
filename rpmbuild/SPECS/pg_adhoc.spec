%global pname pg_adhoc
%global sname pg_filedump
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{pname}
Version:	17.4
Release:	1PGSTY%{?dist}
Summary:	Ad-hoc PostgreSQL diagnostic utilities
License:	GPL-2.0-or-later
URL:		https://github.com/df7cb/pg_filedump
Source0:	pg_filedump-REL_17_4.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	%{sname}%{?_isa} = %{version}-%{release}

%description
pg_adhoc collects standalone PostgreSQL diagnostic utilities. The current
component is pg_filedump, a low-level PostgreSQL data-file inspection tool.

%package -n %{sname}
Summary:	Display formatted contents of a PostgreSQL heap, index, or control file
License:	GPL-2.0-or-later

%description -n %{sname}
pg_filedump is a utility to format PostgreSQL heap/index/control files into a human-readable form.
You can format/dump the files several ways, as listed in the Invocation section, as well as dumping straight binary.

%prep
%setup -q -n %{sname}-REL_17_4

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
cp pg_filedump %{buildroot}/usr/bin/pg_filedump

%files

%files -n %{sname}
%doc README.pg_filedump.md
/usr/bin/pg_filedump

%changelog
* Wed Aug 12 2026 Vonng <rh@vonng.com> - 17.4-1PGSTY
- Package pg_filedump as a component of pg_adhoc

* Thu Nov 20 2025 Vonng <rh@vonng.com> - 17.4
* Sat Sep 23 2023 Vonng <rh@vonng.com> - 17.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
