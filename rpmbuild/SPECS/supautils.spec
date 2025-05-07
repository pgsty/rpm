%define debug_package %{nil}
%global pname supautils
%global sname supautils
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	2.9.1
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension that secures a cluster on a cloud environment
License:	Apache-2.0
URL:		https://github.com/supabase/supautils
Source0:	https://repo.pigsty.cc/ext/%{sname}-%{version}.tar.gz
#           https://github.com/supabase/supautils/archive/refs/tags/v2.9.1.tar.gz
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
install -m 755 build/%{pname}.so %{buildroot}%{pginstdir}/lib/%{pname}.so

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%exclude /usr/lib/.build-id/*

%changelog
* Wed May 07 2025 Vonng <rh@vonng.com> - 2.9.1
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 2.6.0
* Sun Oct 15 2023 Vonng <rh@vonng.com> - 2.5.0
* Mon Oct 14 2023 Vonng <rh@vonng.com> - 2.4.0
* Tue Jul 18 2023 Vonng <rh@vonng.com> - 2.2.1
- Initial RPM release, used by Pigsty <https://pigsty.io>