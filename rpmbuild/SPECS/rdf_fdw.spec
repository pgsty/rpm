%global pname rdf_fdw
%global sname rdf_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.6.0
Release:	1PIGSTY%{?dist}
Summary:	RDF triplestore foreign data wrapper for PostgreSQL
License:	MIT
URL:		https://github.com/jimjonesbr/rdf_fdw
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/rdf_fdw/2.6.0/rdf_fdw-2.6.0.zip
#           Supported: PostgreSQL 9.5+

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libxml2-devel
BuildRequires:	libcurl-devel
BuildRequires:	pkgconf-pkg-config
Requires:	postgresql%{pgmajorversion}-server

%description
rdf_fdw is a PostgreSQL foreign data wrapper for RDF triplestores exposed
through SPARQL endpoints.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
mkdir -p %{_builddir}/%{sname}-%{version}
tar -C %{_builddir}/%{sname}-%{version} --strip-components=1 -xzf %{SOURCE0}
cd %{_builddir}/%{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/rdf_fdw-2.6.0.patch

%build
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Wed Jul 01 2026 Vonng <rh@vonng.com> - 2.6.0-1PIGSTY
- Update to upstream PGXN 2.6.0 and keep EL8 libcurl compatibility patch
- Use system llvm-lto path for builder LLVM version compatibility

* Sun Apr 26 2026 Vonng <rh@vonng.com> - 2.5.0-2PIGSTY
- Add libcurl nghttp2_version compatibility for EL8 builds

* Sat Apr 25 2026 Vonng <rh@vonng.com> - 2.5.0-1PIGSTY
- Update rdf_fdw to upstream PGXN 2.5.0

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 2.4.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
