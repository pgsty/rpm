%define debug_package %{nil}
%global sname hunspell
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:           %{sname}_%{pgmajorversion}
Version:        1.0
Release:        2PIGSTY%{?dist}
Summary:        Hunspell dictionaries for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/postgrespro/hunspell_dicts
Source0:        hunspell-%{version}.tar.gz
Patch0:         hunspell-1.0-pt-stopwords.patch

BuildArch:      noarch
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

Provides:       hunspell_cs_cz_%{pgmajorversion}
Provides:       hunspell_de_de_%{pgmajorversion}
Provides:       hunspell_en_us_%{pgmajorversion}
Provides:       hunspell_fr_%{pgmajorversion}
Provides:       hunspell_ne_np_%{pgmajorversion}
Provides:       hunspell_nl_nl_%{pgmajorversion}
Provides:       hunspell_nn_no_%{pgmajorversion}
Provides:       hunspell_pt_pt_%{pgmajorversion}
Provides:       hunspell_ru_ru_%{pgmajorversion}
Provides:       hunspell_ru_ru_aot_%{pgmajorversion}
Obsoletes:      hunspell_cs_cz_%{pgmajorversion}
Obsoletes:      hunspell_de_de_%{pgmajorversion}
Obsoletes:      hunspell_en_us_%{pgmajorversion}
Obsoletes:      hunspell_fr_%{pgmajorversion}
Obsoletes:      hunspell_ne_np_%{pgmajorversion}
Obsoletes:      hunspell_nl_nl_%{pgmajorversion}
Obsoletes:      hunspell_nn_no_%{pgmajorversion}
Obsoletes:      hunspell_ru_ru_%{pgmajorversion}
Obsoletes:      hunspell_ru_ru_aot_%{pgmajorversion}

%description
Hunspell dictionaries and text search configurations for Czech, German,
English, French, Nepali, Dutch, Norwegian, Portuguese, and Russian.

This package contains the following PostgreSQL extensions:
hunspell_cs_cz, hunspell_de_de, hunspell_en_us, hunspell_fr,
hunspell_ne_np, hunspell_nl_nl, hunspell_nn_no, hunspell_pt_pt,
hunspell_ru_ru, and hunspell_ru_ru_aot.

%prep
%setup -q -n hunspell-%{version}
%patch0 -p1
%{__mv} hunspell_pt_pt/portuguese.stop hunspell_pt_pt/pt_pt.stop
for dictionary in \
    hunspell_cs_cz hunspell_de_de hunspell_en_us hunspell_fr \
    hunspell_ne_np hunspell_nl_nl hunspell_nn_no hunspell_pt_pt \
    hunspell_ru_ru hunspell_ru_ru_aot; do
    %{__mv} "${dictionary}/license" "${dictionary}/${dictionary}-license"
done

%install
%{__rm} -rf %{buildroot}
for dictionary in \
    hunspell_cs_cz hunspell_de_de hunspell_en_us hunspell_fr \
    hunspell_ne_np hunspell_nl_nl hunspell_nn_no hunspell_pt_pt \
    hunspell_ru_ru hunspell_ru_ru_aot; do
    PATH=%{pginstdir}/bin:$PATH %{__make} -C "${dictionary}" \
        USE_PGXS=1 install DESTDIR=%{buildroot}
done

%files
%license LICENSE hunspell_*/hunspell_*-license
%doc README.md
%{pginstdir}/share/extension/hunspell_*.control
%{pginstdir}/share/extension/hunspell_*--*.sql
%{pginstdir}/share/tsearch_data/*.affix
%{pginstdir}/share/tsearch_data/*.dict
%{pginstdir}/share/tsearch_data/*.stop

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 1.0-2PIGSTY
- Merge all dictionaries into the hunspell package
- Rename the bundled Portuguese stopword file to avoid PostgreSQL conflicts

* Thu Jul 18 2024 Vonng <rh@vonng.com> - 1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
