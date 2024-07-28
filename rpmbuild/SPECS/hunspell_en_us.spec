%define debug_package %{nil}
%global pname hunspell_en_us
%global sname hunspell_en_us
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1PIGSTY%{?dist}
Summary:	Hunspell dictionaries for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/postgrespro/hunspell_dicts
Source0:	hunspell-1.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
The repository contains hunspell dictionaries for several languages listed below.
hunspell_cs_cz	czech_hunspell
hunspell_de_de	german_hunspell
hunspell_en_us	english_hunspell
hunspell_fr	    french_hunspell
hunspell_ne_np	nepali_hunspell
hunspell_nl_nl	dutch_hunspell
hunspell_nn_no	norwegian_hunspell
hunspell_pt_pt	portuguese_hunspell
hunspell_ru_ru	russian_hunspell
hunspell_ru_ru_aot	russian_aot_hunspell

%prep
%setup -q -n hunspell-%{version}

%install
%{__rm} -rf %{buildroot}
cd %{pname}
PATH=%{pginstdir}/bin:$PATH make USE_PGXS=1 install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/tsearch_data/*

%exclude /usr/lib/.build-id/*

%changelog
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>