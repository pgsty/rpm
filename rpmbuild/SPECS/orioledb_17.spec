%global sname orioledb
%global pname orioledb
%global pgmajorversion 17
%global pginstdir	/usr/oriole-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.0
Release:	10PIGSTY%{?dist}
Summary:	Modern cloud-native storage engine for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/orioledb/orioledb
Source0:	%{sname}-beta10.tar.gz

BuildRequires:	oriolepg_%{pgmajorversion} >= 17.0
Requires:	    oriolepg_%{pgmajorversion} >= 17.0

%description
OrioleDB – building a modern cloud-native storage engine, and solving some PostgreSQL wicked problems
This is the extension package for OrioleDB modfied postgres 17

%prep
%setup -q -n %{sname}-beta10

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
* Sat Apr 05 2025 Ruohang Feng (Vonng) <rh@vonng.com> - 0.0.0-10PIGSTY
- Initial RPM release, beta10 version, used by Pigsty <https://pigsty.io>