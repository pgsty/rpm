%global pname pg_sorted_heap
%global sname pg_sorted_heap
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16
%{error:pg_sorted_heap only supports PostgreSQL 16+}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.14.0
Release:	1PIGSTY%{?dist}
Summary:	Sorted heap table access method with zone-map pruning
License:	PostgreSQL
URL:		https://github.com/skuznetsov/pg_sorted_heap
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_sorted_heap/0.14.0/pg_sorted_heap-0.14.0.zip
#           Supported: PostgreSQL 16, 17, 18

BuildRequires:	gcc
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_sorted_heap is a PostgreSQL table access method that physically sorts heap
storage by primary key, prunes heap blocks with zone maps, and includes vector
types plus planner-integrated HNSW search.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} with_llvm=no

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} with_llvm=no

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 04 2026 Vonng <rh@vonng.com> - 0.14.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.14.0
