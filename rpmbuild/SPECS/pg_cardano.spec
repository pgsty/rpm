%define debug_package %{nil}
%global pname pg_cardano
%global sname pg_cardano
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.5
Release:	1PIGSTY%{?dist}
Summary:	Cardano-related tools, including cryptographic functions, address encoding/decoding, and blockchain data processing.
License:	MIT
URL:		https://github.com/Fell-x27/pg_cardano
Source0:	pg_cardano-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
This extension is an attempt to create a Swiss Army knife for simplifying the work with binary data in Cardano db-sync, as well as automating some processes.
It is written in Rust, which ensures high security and excellent performance.
The extension is designed to handle unforeseen errors gracefully, without causing any disruptions in the database's operation. All errors are safely propagated as PostgreSQL-level error messages.

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
* Wed May 07 2025 Vonng <rh@vonng.com> - 1.0.5
* Wed Dec 10 2024 Vonng <rh@vonng.com> - 1.0.3
* Sat Oct 19 2024 Vonng <rh@vonng.com> - 1.0.2
- Initial RPM release, used by Pigsty <https://pigsty.io>