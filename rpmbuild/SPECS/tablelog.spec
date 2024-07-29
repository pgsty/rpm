%define debug_package %{nil}
%global pname tablelog
%global sname tablelog
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1
Release:	1PIGSTY%{?dist}
Summary:	A PostgreSQL extension for capturing table modifications with table trigger
License:	BSD 2-Clause
URL:		https://github.com/snaga/tablelog
Source0:	tablelog-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server plv8_%{pgmajorversion}

%description
tablelogは、テーブルへの更新処理（INSERT/UPDATE/DELETE）をログとして記 録するためのPostgreSQLの拡張モジュール（extension）です。
tablelogは、各テーブルに設定したトリガを使って、当該テーブルへの更新処 理を記録用のテーブルに保存します。
tablelogを使うことによって、テーブルへの更新内容を後から確認、または再 生することでテーブルの複製やデータベースの移行に利用することができます。


%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 0.1
- Initial RPM release, used by Pigsty <https://pigsty.io>