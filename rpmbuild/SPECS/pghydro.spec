%global pname pghydro
%global sname pghydro
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	6.6
Release:	1PIGSTY%{?dist}
Summary:	Drainage network analysis extensions for PostgreSQL and PostGIS
License:	GPL-2.0-only
URL:		https://github.com/pghydro/pghydro
Source0:	%{sname}-%{version}.tar.gz
#           repacked from upstream release https://github.com/pghydro/pghydro/releases/tag/v.6.6x

BuildRequires:	pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgis36_%{pgmajorversion}

%description
PgHydro is a SQL-only bundle of PostgreSQL and PostGIS extensions for drainage
network analysis and water-resources decision support. This package installs
pghydro, pgh_raster, pgh_hgm, pgh_output, pgh_output_en_au,
pgh_output_pt_br, and pgh_consistency. Runtime use requires PostGIS and
PostGIS Raster to be installed before the PgHydro extensions are created.

%prep
%setup -q -n %{sname}-v.%{version}x

%build
# Pure SQL extension bundle, nothing to compile.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
install -m 0644 pghydro.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_raster.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_hgm.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_output.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_output_en_au.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_output_pt_br.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_consistency.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pghydro--6.6.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_raster--6.6.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_hgm--2.2.6.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_output--6.6.sql %{buildroot}%{pginstdir}/share/extension/
# Upstream ships the en-au SQL file with a UTF-8 BOM; strip it while mapping
# the filename to the underscore-based extension name.
tail -c +4 pgh_output_en-au--6.6.sql > %{buildroot}%{pginstdir}/share/extension/pgh_output_en_au--6.6.sql
install -m 0644 pgh_output_pt_br--6.6.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 pgh_consistency--6.6.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 README.md Description.pdf pghydro--6.6_README.txt pghydro--6.6_tutorial.sql pgh_hgm--2.2.6-tutorial.sql %{buildroot}%{_docdir}/%{name}/
install -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/Description.pdf
%doc %{_docdir}/%{name}/pghydro--6.6_README.txt
%doc %{_docdir}/%{name}/pghydro--6.6_tutorial.sql
%doc %{_docdir}/%{name}/pgh_hgm--2.2.6-tutorial.sql
%{pginstdir}/share/extension/pghydro.control
%{pginstdir}/share/extension/pghydro--6.6.sql
%{pginstdir}/share/extension/pgh_raster.control
%{pginstdir}/share/extension/pgh_raster--6.6.sql
%{pginstdir}/share/extension/pgh_hgm.control
%{pginstdir}/share/extension/pgh_hgm--2.2.6.sql
%{pginstdir}/share/extension/pgh_output.control
%{pginstdir}/share/extension/pgh_output--6.6.sql
%{pginstdir}/share/extension/pgh_output_en_au.control
%{pginstdir}/share/extension/pgh_output_en_au--6.6.sql
%{pginstdir}/share/extension/pgh_output_pt_br.control
%{pginstdir}/share/extension/pgh_output_pt_br--6.6.sql
%{pginstdir}/share/extension/pgh_consistency.control
%{pginstdir}/share/extension/pgh_consistency--6.6.sql

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 6.6-1PIGSTY
- Package upstream release v.6.6x carrying PgHydro 6.6 SQL extensions
