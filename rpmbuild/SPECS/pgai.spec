%define debug_package %{nil}
%global pname pgai
%global sname pgai
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.8.1
Release:	1PIGSTY%{?dist}
Summary:	Bring AI models to PostgreSQL with pgai
License:	PostgreSQL
URL:		https://github.com/timescale/pgai
Source0:	pgai-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pgai is a PostgreSQL extension that brings AI models closer to your data.
It enables vector embeddings generation, semantic search, and RAG capabilities
directly within PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Fri Jan 17 2026 Vonng <rh@vonng.com> - 0.8.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>