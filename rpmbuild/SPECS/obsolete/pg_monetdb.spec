# Obsolete in PGSTY builds: active EL builder repos do not ship monetdb-devel.
%global pname pg_monetdb
%global sname pg_monetdb
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15
%{error:pg_monetdb only supports PostgreSQL 15+}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	1PIGSTY%{?dist}
Summary:	MonetDB foreign data wrapper for PostgreSQL
License:	MPL-2.0
URL:		https://github.com/saulojb/pg_monetdb
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_monetdb/1.4.0/pg_monetdb-1.4.0.zip
#           Supported: PostgreSQL 15, 16, 17, 18

BuildRequires:	gcc monetdb-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_monetdb is a PostgreSQL foreign data wrapper for querying and modifying
data stored in remote MonetDB servers, with analytical pushdown support.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} \
    MONETDB_LIB=/usr/lib64 MONETDB_INCLUDE=/usr/include/monetdb with_llvm=no

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install \
    DESTDIR=%{buildroot} MONETDB_LIB=/usr/lib64 MONETDB_INCLUDE=/usr/include/monetdb with_llvm=no

%files
%doc README.md README_cn.md README_pt_BR.md RELEASE_v1.4.0.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 04 2026 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.4.0
