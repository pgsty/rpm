%global pname pg_filedump
%global sname pg_filedump
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}
Version:	16.0
Release:	1PIGSTY%{?dist}
Summary:	Display formatted contents of a PostgreSQL heap, index, or control file
License:	GPL v2.0+
URL:		https://github.com/df7cb/%{sname}
Source0:	https://github.com/df7cb/%{sname}/archive/refs/tags/pg_filedump-REL_16_0.tar.gz
#           https://github.com/df7cb/pg_filedump/archive/refs/tags/REL_16_0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27

%description
pg_filedump is a utility to format PostgreSQL heap/index/control files into a human-readable form.
You can format/dump the files several ways, as listed in the Invocation section, as well as dumping straight binary.

%prep
%setup -q -n %{sname}-REL_16_0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
cp pg_filedump %{buildroot}/usr/bin/pg_filedump

%files
/usr/bin/pg_filedump
%exclude /usr/lib/.build-id/*

%changelog
* Sat Sep 23 2023 Vonng <rh@vonng.com> - 16.0
- Initial RPM release, used by Pigsty <https://pigsty.io>