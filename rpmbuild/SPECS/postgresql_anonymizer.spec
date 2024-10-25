%global sname postgresql_anonymizer
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.3.2
Release:	1PIGSTY%{?dist}
Summary:	Anonymization & Data Masking for PostgreSQL
License:	PostgreSQL
URL:		https://gitlab.com/dalibo/postgresql_anonymizer
Source0:	postgresql_anonymizer-%{version}.tar.gz
#Source0:   https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
Requires:	ddlx_%{pgmajorversion}

%description
postgresql_anonymizer is an extension to mask or replace personally
identifiable information (PII) or commercially sensitive data from a
PostgreSQL database.

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
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE.md
%defattr(644,root,root,755)
%{pginstdir}/bin/pg_dump_anon.sh
%{pginstdir}/lib/anon.so
%{pginstdir}/share/extension/anon/*
%{pginstdir}/share/extension/anon.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc docs/*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/anon*.bc
   %{pginstdir}/lib/bitcode/anon/*.bc
%endif


%changelog
* Wed Oct 11 2023 Vonng <rh@vonng.com> - 1.3.2
- Initial RPM release, used by Pigsty <https://pigsty.io>