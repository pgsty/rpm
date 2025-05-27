%define debug_package %{nil}
%global pname pg_tokenizer
%global sname pg_tokenizer.rs
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{pname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL tokenizer extension for full-text search
License:	Apache-2.0
URL:		https://github.com/tensorchord/%{sname}
SOURCE0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
A PostgreSQL extension that provides tokenizers for full-text search.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Mon May 26 2025 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>