%global pname pgelog
%global sname pgelog
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.2
Release:	1PIGSTY%{?dist}
Summary:	Extended PostgreSQL logging via pseudo-autonomous transactions
License:	PostgreSQL
URL:		https://github.com/anfiau/pgelog
Source0:	%{sname}-%{version}.zip
#           https://api.pgxn.org/dist/pgelog/1.0.2/pgelog-1.0.2.zip
#           Supported: PostgreSQL 11+
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	unzip
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib pg_variables_%{pgmajorversion}

%description
pgelog is a PostgreSQL extension for extended logging through
pseudo-autonomous transactions using dblink into a log table.

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
cd %{_builddir}
unzip -q %{SOURCE0}

%build
# Pure SQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%changelog
* Sun Apr 05 2026 Vonng <rh@vonng.com> - 1.0.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
