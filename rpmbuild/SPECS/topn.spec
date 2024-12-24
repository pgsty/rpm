%global sname topn

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension that returns the top values in a database
Name:		%{sname}_%{pgmajorversion}
Version:	2.7.0
Release:	1PGDG%{dist}
License:	AGPLv3
Source0:    postgresql-topn-2.7.0.tar.gz
#Source0:	https://github.com/citusdata/postgresql-%{sname}/archive/v%{version}.tar.gz

URL:		https://github.com/citusdata/postgresql-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description
TopN is an open source PostgreSQL extension that returns the top values
in a database according to some criteria. TopN takes elements in a data
set, ranks them according to a given rule, and picks the top elements in
that data set. When doing this, TopN applies an approximation algorithm
to provide fast results using few compute and memory resources.

The TopN extension becomes useful when you want to materialize top
values, incrementally update these top values, and/or merge top values
from different time intervals. If you're familiar with the PostgreSQL
HLL extension, you can think of TopN as its cousin.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for topn
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 13.0 clang-devel >= 13.0
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for topn
%endif

%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif


%changelog
* Tue Dec 24 2024 Vonng <rh@vonng.com> - 2.17.2
- Initial RPM release, used by Pigsty <https://pigsty.io>
* Sat Oct 19 2024 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1PGDG
- Update to 2.7.0
* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository.
