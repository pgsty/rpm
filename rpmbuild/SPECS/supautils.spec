%define debug_package %{nil}
%global pname supautils
%global sname supautils
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	3.1.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension that secures a cluster on a cloud environment
License:	Apache-2.0
URL:		https://github.com/supabase/supautils
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/supabase/supautils/archive/refs/tags/v3.1.0.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Supautils is an extension that secures a PostgreSQL cluster on a cloud environment.
It doesn't require creating database objects. It's a shared library that modifies PostgreSQL behavior through "hooks",
not through tables or functions.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
install -d -m 755 %{buildroot}%{pginstdir}/lib/
install -m 755 %{pname}.so %{buildroot}%{pginstdir}/lib/%{pname}.so

%files
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%changelog
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