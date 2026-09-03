%global pname rdf_fdw
%global sname rdf_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:rdf_fdw only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.7.0
Release:	1PGSTY%{?dist}
Summary:	RDF triplestore foreign data wrapper for PostgreSQL
License:	MIT
URL:		https://github.com/jimjonesbr/rdf_fdw
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/rdf_fdw/2.7.0/rdf_fdw-2.7.0.zip
#           Supported: PostgreSQL 9.5+

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libxml2-devel
BuildRequires:	libcurl-devel
BuildRequires:	pkgconf-pkg-config
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
rdf_fdw is a PostgreSQL foreign data wrapper for RDF triplestores exposed
through SPARQL endpoints.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/rdf_fdw-2.7.0.patch

%build
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.7.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Restore automatic debuginfo and debugsource generation with %setup

* Mon Jul 27 2026 Vonng <rh@vonng.com> - 2.7.0-1PIGSTY
- Update to upstream PGXN 2.7.0 and refresh the EL8 libcurl patch

* Wed Jul 01 2026 Vonng <rh@vonng.com> - 2.6.0-1PIGSTY
- Update to upstream PGXN 2.6.0 and keep EL8 libcurl compatibility patch
- Use system llvm-lto path for builder LLVM version compatibility

* Sun Apr 26 2026 Vonng <rh@vonng.com> - 2.5.0-2PIGSTY
- Add libcurl nghttp2_version compatibility for EL8 builds

* Sat Apr 25 2026 Vonng <rh@vonng.com> - 2.5.0-1PIGSTY
- Update rdf_fdw to upstream PGXN 2.5.0

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 2.4.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
