%define debug_package %{nil}
%global pname vectorize
%global sname pg_vectorize
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.17.0
Release:	1PIGSTY%{?dist}
Summary:	The simplest way to orchestrate vector search on Postgres
License:	PostgreSQL
URL:		https://github.com/tembo-io/pg_vectorize
SOURCE0:    pg_vectorize-%{version}.tar.gz
#           https://github.com/tembo-io/pg_vectorize/archive/refs/tags/v0.17.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pgmq_%{pgmajorversion} >= 1.1.1
Recommends: pg_cron_%{pgmajorversion}

%description
A Postgres extension that automates the transformation and orchestration of text to embeddings and provides hooks into the most popular LLMs.
This allows you to do vector search and build LLM applications on existing data with as little as two function calls.

%prep
%setup -q -n %{sname}-%{version}

%build
cd extension
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.17.0
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 0.16.0
* Sun May 5 2024 Vonng <rh@vonng.com> - 0.15.0
- Initial RPM release, used by Pigsty <https://pigsty.io>