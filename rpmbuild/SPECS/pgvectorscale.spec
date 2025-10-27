%define debug_package %{nil}
%global pname vectorscale
%global sname pgvectorscale
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.8.0
Release:	1PIGSTY%{?dist}
Summary:	A complement to pgvector for high performance, cost efficient vector search on large workloads.
License:	PostgreSQL
URL:		https://github.com/timescale/pgvectorscale
SOURCE0:    pgvectorscale-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pgvector_%{pgmajorversion} >= 0.7.0

%description
pgvectorscale builds on pgvector with higher performance embedding search and cost-efficient storage for AI applications.

%prep
%setup -q -n %{sname}-%{version}

%build
export PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH
export RUSTFLAGS="-C target-feature=+avx2,+fma"
cd pgvectorscale
cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}-%{version}.so       %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 0.8.0
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.7.1
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.6.0
- https://github.com/timescale/pgvectorscale/releases/tag/0.6.0
* Tue Dec 10 2024 Vonng <rh@vonng.com> - 0.5.1
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.4.0
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 0.2.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>