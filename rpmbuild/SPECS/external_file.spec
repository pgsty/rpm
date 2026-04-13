%global pname external_file
%global sname external_file
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.2
Release:	1PIGSTY%{?dist}
Summary:	Access external server-side files through PostgreSQL functions
License:	PostgreSQL
URL:		https://github.com/darold/external_file
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/darold/external_file/archive/refs/tags/v1.2.tar.gz
BuildArch:	noarch

BuildRequires:	pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
external_file adds an Oracle BFILE-like data type and helper functions that
read or write files on the PostgreSQL server filesystem through controlled
server-side large-object APIs. The extension installs into the fixed
external_file schema and requires superuser privileges to create.

%prep
%setup -q -n %{sname}-%{version}

%build
# Pure SQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
install -m 0644 external_file.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 external_file--*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 updates/external_file--*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 README.md README.external_file CHANGELOG %{buildroot}%{_docdir}/%{name}/
install -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/README.external_file
%doc %{_docdir}/%{name}/CHANGELOG
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.2-1PIGSTY
- Initial RPM release based on upstream tag v1.2
