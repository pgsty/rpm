%global pname supautils
%global sname supautils
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:supautils 3.4.3 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	3.4.3
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension that secures a cluster on a cloud environment
License:	Apache-2.0 AND PostgreSQL AND LicenseRef-Public-Domain
URL:		https://github.com/supabase/supautils
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/supabase/supautils/archive/refs/tags/v3.4.3.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Supautils is an extension that secures a PostgreSQL cluster on a cloud environment.
It doesn't require creating database objects. It's a shared library that modifies PostgreSQL behavior through "hooks",
not through tables or functions.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Thu Sep 03 2026 Vonng <rh@vonng.com> - 3.4.3-1PGSTY
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Update to upstream supautils 3.4.3
- Align LLVM dependencies and package the complete PGXS bitcode payload

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 3.4.2-1PGSTY
- Bump to 3.4.2

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 3.2.1-1PIGSTY
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 3.1.0-1PIGSTY
* Fri Oct 31 2025 Vonng <rh@vonng.com> - 3.0.2-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 3.0.1-1PIGSTY
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 2.10.0-1PIGSTY
* Fri May 23 2025 Vonng <rh@vonng.com> - 2.9.2-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 2.9.1-1PIGSTY
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 2.6.0-1PIGSTY
* Sun Oct 15 2023 Vonng <rh@vonng.com> - 2.5.0-1PIGSTY
* Sat Oct 14 2023 Vonng <rh@vonng.com> - 2.4.0-1PIGSTY
* Tue Jul 18 2023 Vonng <rh@vonng.com> - 2.2.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
