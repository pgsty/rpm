%global sname pllua
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global plluangmajver 2
%global plluangmidver 0
%global plluangminver 12

%{!?llvm:%global llvm 1}

Summary:	Procedural language interface between PostgreSQL and Lua
Name:		%{sname}_%{pgmajorversion}
Version:	%{plluangmajver}.%{plluangmidver}.%{plluangminver}
Release:	4PIGSTY%{?dist}
License:	MIT
Source0:	%{sname}-%{version}.tar.gz
%if 0%{?pgmajorversion} >= 18
Patch0:		pllua-pg18-noreturn.patch
%endif
URL:		https://github.com/%{sname}/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	lua-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	lua-libs

%description
PL/Lua is a procedural language module for PostgreSQL that allows
server-side functions to be written in Lua.

%package devel
Summary:	PL/Lua development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes development libraries for PL/Lua.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pllua
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires:	llvm-devel >= 13.0 clang-devel >= 13.0
Requires:	llvm >= 13.0

%description llvmjit
This package provides JIT support for pllua.
%endif

%prep
%setup -q -n %{sname}-REL_%{plluangmajver}_%{plluangmidver}_%{plluangminver}
%if 0%{?pgmajorversion} >= 18
%patch -P 0 -p1
%endif

%build
LUALIB="-L%{libdir} -l lua" LUAC="%{_bindir}/luac" LUA="%{_bindir}/lua" \
	PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
LUALIB="-L%{libdir} -l lua" LUAC="%{_bindir}/luac" LUA="%{_bindir}/lua" \
	PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} \
	install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE
%defattr(644,root,root,755)
%{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}u*.sql
%{pginstdir}/share/extension/%{sname}u.control

%files devel
%dir %{pginstdir}/include/server/extension/%{sname}
%{pginstdir}/include/server/extension/%{sname}/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*.bc
%dir %{pginstdir}/lib/bitcode/%{sname}
%{pginstdir}/lib/bitcode/%{sname}/*
%endif

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 2.0.12-4PIGSTY
- Add PostgreSQL 18 compatibility

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.12-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support
