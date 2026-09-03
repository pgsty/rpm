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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	4.4.2
Release:	1PGSTY%{?dist}
Summary:	Clone PostgreSQL databases, schemas, and tables across environments
License:	PostgreSQL
URL:		https://github.com/valehdba/pgclone
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgclone/4.4.2/pgclone-4.4.2.zip
#           Supported: PostgreSQL 14, 15, 16, 17, 18

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pgclone is a PostgreSQL extension written in C that clones databases, schemas,
tables, and functions between PostgreSQL instances directly from SQL.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}
install -m 644 README.md CHANGELOG.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 4.4.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 4.4.2-1PIGSTY
- Update to upstream PGXN 4.4.2

* Thu May 14 2026 Vonng <rh@vonng.com> - 4.3.2-1PIGSTY
- Update to upstream PGXN 4.3.2 with the normalized pgclone-4.3.2.tar.gz source tarball

* Thu Apr 16 2026 Vonng <rh@vonng.com> - 4.0.0-1PIGSTY
- Update to upstream 4.0.0 with the normalized pgclone-4.0.0.tar.gz source tarball
- Track the upstream schema-namespace breaking change in the packaged extension

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 3.6.0-1PIGSTY
- Update to upstream 3.6.0 with the normalized pgclone-3.6.0.tar.gz source tarball

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 2.2.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
