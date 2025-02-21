%define debug_package %{nil}
%global pname vchord
%global sname vchord
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.1
Release:	1PIGSTY%{?dist}
Summary:	Scalable, Fast, and Disk-friendly Vector search in Postgres, the Successor of pgvecto.rs.
License:	AGPL-3.0
URL:		https://github.com/tensorchord/VectorChord
Source0:	VectorChord-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pgvector_%{pgmajorversion} >= 0.7.0

%description
VectorChord (vchord) is a PostgreSQL extension designed for scalable, high-performance, and disk-efficient vector similarity search, and serves as the successor to pgvecto.rs.

%prep
%setup -q -n VectorChord-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/VectorChord-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/VectorChord-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/VectorChord-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.2.1
* Mon Feb 10 2025 Vonng <rh@vonng.com> - 0.2.0
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>