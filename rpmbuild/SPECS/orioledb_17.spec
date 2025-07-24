%global sname orioledb
%global pname orioledb
%global pgmajorversion 17
%global pginstdir	/usr/oriole-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.5
Release:	0.beta12PIGSTY%{?dist}
Summary:	Modern cloud-native storage engine for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/orioledb/orioledb
Source0:	%{sname}-beta12.tar.gz

BuildRequires:	oriolepg_%{pgmajorversion} >= 17.11 libcurl-devel
Requires:	    oriolepg_%{pgmajorversion} >= 17.11

%description
OrioleDB – building a modern cloud-native storage engine, and solving some PostgreSQL wicked problems
This is the extension package for OrioleDB modified postgres 17

%prep
%setup -q -n %{sname}-beta12

%build
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/postgresql/%{pname}.so
%{pginstdir}/share/postgresql/extension/%{pname}.control
%{pginstdir}/share/postgresql/extension/%{pname}*sql
%{pginstdir}/lib/postgresql/bitcode/*
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jul 24 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.5-0.beta12PIGSTY
* Tue May 27 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.4-0.beta11PIGSTY
* Sat Apr 05 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 1.4-0.beta10PIGSTY
- Initial RPM release, beta10 version, used by Pigsty <https://pigsty.io>