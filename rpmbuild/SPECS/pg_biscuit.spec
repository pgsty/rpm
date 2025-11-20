%global pname pg_biscuit
%global sname pg_biscuit
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1PIGSTY%{?dist}
Summary:	IAM-LIKE pattern matching with bitmap indexing
License:	MIT
URL:		https://github.com/CrystallineCore/pg_biscuit
Source0:	pg_biscuit-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
pg_biscuit is a PostgreSQL Index Access Method (IAM) for high-performance pattern matching
on text columns. Biscuit indexes are specifically designed to accelerate LIKE queries with
arbitrary wildcards using roaring bitmaps. It provides superior performance for wildcard
pattern matching compared to traditional B-tree, GIN, or GiST indexes, especially for
queries with leading wildcards like '%%pattern%%'.

%prep
%setup -q -n pg_biscuit-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Nov 18 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>