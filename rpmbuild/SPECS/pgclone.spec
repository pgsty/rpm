%global pname pgclone
%global sname pgclone
%global pginstdir /usr/pgsql-%{pgmajorversion}

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
Version:	4.0.0
Release:	1PIGSTY%{?dist}
Summary:	Clone PostgreSQL databases, schemas, and tables across environments
License:	PostgreSQL
URL:		https://github.com/valehdba/pgclone
Source0:	%{sname}-%{version}.tar.gz
#           normalized source tarball from https://github.com/valehdba/pgclone/releases/tag/v4.0.0
#           Supported: PostgreSQL 14, 15, 16, 17, 18

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pgclone is a PostgreSQL extension written in C that clones databases, schemas,
tables, and functions between PostgreSQL instances directly from SQL.

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
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
install -m 644 README.md CHANGELOG.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Thu Apr 16 2026 Vonng <rh@vonng.com> - 4.0.0-1PIGSTY
- Update to upstream 4.0.0 with the normalized pgclone-4.0.0.tar.gz source tarball
- Track the upstream schema-namespace breaking change in the packaged extension

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 3.6.0-1PIGSTY
- Update to upstream 3.6.0 with the normalized pgclone-3.6.0.tar.gz source tarball

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 2.2.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
