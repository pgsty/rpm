%define debug_package %{nil}
%global pname pgfaceting
%global sname pgfaceting
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	A custom data type for storing MD5 hashes (instead of the native TEXT varlena type).
License:	BSD 3-Clause
URL:		https://github.com/cybertec-postgresql/pgfaceting
Source0:	pgfaceting-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pg_roaringbitmap_%{pgmajorversion} >= 0.5

%description
PostgreSQL extension to quickly calculate facet counts using inverted index built with roaring bitmaps. Requires pg_roaringbitmap to be installed.
Faceting means counting number occurrences of each value in a result set for a set of attributes. Typical example of faceting is a web shop where you can see how many items are remaining after filtering your search by red, green or blue, and how many when filtering by size small, medium or large.
Work on this project has been sponsored by Xenit.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 0.2.0
- Initial RPM release, used by Pigsty <https://pigsty.io>