%global sname	login_hook
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}


Name:		%{sname}_%{pgmajorversion}
Version:	1.7
Release:	3PIGSTY%{?dist}
Summary:	Postgres database extension to execute some code on user login, comparable to Oracle's after logon trigger.
License:	GPL-3.0
URL:		https://github.com/splendiddata/%{sname}
Source0:	%{sname}-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Postgres database extension to execute some code on user login,
comparable to Oracle's after logon trigger.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for login_hook
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for login_hook
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
# No need to ship these files:
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.css
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.html

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Nov 01 2025 Vonng <rh@vonng.com> - 1.7.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>