%global pname pg_slug_gen
%global sname pg_slug_gen
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15
%{error:pg_slug_gen only supports PostgreSQL 15+}
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
Version:	1.0.0
Release:	1PGSTY%{?dist}
Summary:	Generate random timestamp-based slugs in PostgreSQL
License:	MIT
URL:		https://github.com/nandoolle/pg_slug_gen
Source0:	%{sname}-%{version}.tar.gz
#           normalized source tarball from the upstream GitHub tag archive
#           Supported: PostgreSQL 14+

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_slug_gen is a PostgreSQL extension for generating random slugs based on
timestamps with cryptographically secure character selection.

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
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude %{pginstdir}/doc/extension/README.md
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Restore automatic debuginfo and debugsource generation with %setup

* Mon Apr 06 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Restrict builds to PostgreSQL 15+ after EL10A validation

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
