%define debug_package %{nil}
%global pname pg_jieba
%global sname pg_jieba
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_jieba supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.1
Release:	1PIGSTY%{?dist}
Summary:	Chinese full-text search parser for PostgreSQL
License:	BSD-3-Clause AND MIT
URL:		https://github.com/jaiminpan/pg_jieba
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/jaiminpan/pg_jieba/archive/refs/tags/v2.0.1.tar.gz
#           The source archive vendors cppjieba submodule commit
#           45809955f5a345886ec3d49cbed3ec68ced70b1c.
Patch0:		pg_jieba-2.0.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cmake gcc-c++
Requires:	postgresql%{pgmajorversion}-server

%description
pg_jieba is a PostgreSQL extension for Chinese full-text search. It embeds
the cppjieba tokenizer and provides text search parsers, configurations,
dictionaries, and query segmentation support.

%prep
%autosetup -p1 -n %{sname}-%{version}
cp -p libjieba/LICENSE cppjieba-LICENSE

%build
mkdir -p build
cd build
PATH=%{pginstdir}/bin:$PATH cmake .. \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{pginstdir} \
    -DPostgreSQL_INCLUDE_DIR=%{pginstdir}/include \
    -DPostgreSQL_TYPE_INCLUDE_DIR=%{pginstdir}/include/server \
    -DPostgreSQL_LIBRARY=%{pginstdir}/lib/libpq.so
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd build
%{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE cppjieba-LICENSE
%doc README.md HISTORY
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/tsearch_data/jieba.dict.utf8
%{pginstdir}/share/tsearch_data/jieba.hmm_model.utf8
%{pginstdir}/share/tsearch_data/jieba.user.dict.utf8
%{pginstdir}/share/tsearch_data/jieba.stop
%{pginstdir}/share/tsearch_data/jieba.idf.utf8
%exclude /usr/lib/.build-id/*

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 2.0.1-1PIGSTY
- Initial RPM release with the pinned cppjieba submodule
